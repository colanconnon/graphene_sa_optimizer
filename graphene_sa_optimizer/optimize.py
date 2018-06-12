from graphene.utils.str_converters import to_snake_case
from sqlalchemy import inspect
from sqlalchemy.orm import joinedload, load_only
from sqlalchemy.orm.properties import RelationshipProperty


def model_fields_as_dict(model):
    return dict((column.key, column) for column in inspect(model).attrs)


def find_model_selections(ast):
    selections = ast.selection_set.selections

    for selection in selections:
        if selection.name.value == "edges":
            for sub_selection in selection.selection_set.selections:
                if sub_selection.name.value == "node":
                    return sub_selection.selection_set.selections

    return selections


def get_related_fetches_for_model(model, graphql_ast):
    model_fields = model_fields_as_dict(model)
    selections = find_model_selections(graphql_ast)
    # optimizations = {}
    # if graphene_obj_type and graphene_obj_type._meta.optimizations:
    #     optimizations = graphene_obj_type._meta.optimizations

    joined_loads = []
    fields = {}
    for selection in selections:
        selection_name = to_snake_case(selection.name.value)
        selection_field = model_fields.get(selection_name, None)
        try:
            if not isinstance(selection_field, RelationshipProperty):
                if graphql_ast.name.value not in fields:
                    fields[graphql_ast.name.value] = []
                fields[graphql_ast.name.value].append(selection_field.key)
                continue
        except Exception as e:
            continue
        joined_loads.append(selection_field.key)
        nested_relateds, nested_fields = get_related_fetches_for_model(
            selection_field.mapper.class_, selection
        )
        if nested_relateds:
            for related in nested_relateds:
                full_name = "{0}.{1}".format(selection_field.key, related)
                joined_loads.append(full_name)
        if nested_fields:
            for key, value in nested_fields.items():
                full_name = "{0}.{1}".format(graphql_ast.name.value, key)
                fields[full_name] = value
    return joined_loads, fields


def get_optimized_joins(model, graphql_info):
    base_ast = graphql_info.field_asts[0]
    joins, fields = get_related_fetches_for_model(model, base_ast)
    return [
        joinedload(name).load_only(*fields[model.__tablename__ + "." + name])
        for name in joins
    ] + [load_only(*fields[model.__tablename__])]
