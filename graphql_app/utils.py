from graphene.utils.str_converters import to_snake_case
from sqlalchemy import inspect
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.properties import RelationshipProperty


def model_fields_as_dict(model):
    return dict((column.key, column) for column in inspect(model).attrs)
    
def find_model_selections(ast):
    selections = ast.selection_set.selections

    for selection in selections:
        if selection.name.value == 'edges':
            for sub_selection in selection.selection_set.selections:
                if sub_selection.name.value == 'node':
                    return sub_selection.selection_set.selections

    return selections


def get_related_fetches_for_model(model, graphql_ast):
    model_fields = model_fields_as_dict(model)
    selections = find_model_selections(graphql_ast)
    # optimizations = {}
    # if graphene_obj_type and graphene_obj_type._meta.optimizations:
    #     optimizations = graphene_obj_type._meta.optimizations

    joined_loads = []
    for selection in selections:
        selection_name = to_snake_case(selection.name.value)
        selection_field = model_fields.get(selection_name, None)
        try:
            if not isinstance(selection_field, RelationshipProperty):
                continue
        except:
            continue
        joined_loads.append(selection_field.key)
        nested_relateds = get_related_fetches_for_model(
            selection_field.mapper.class_, selection)

        if nested_relateds:
            for related in nested_relateds:
                full_name = '{0}.{1}'.format(selection_field.key, related)
                joined_loads.append(full_name)
    return joined_loads


def get_optimized_joins(model, graphql_info):
    base_ast = graphql_info.field_asts[0]
    return [joinedload(name) for name in get_related_fetches_for_model(model, base_ast)] 
