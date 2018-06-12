from graphql import (
    ResolveInfo,
    Source,
    Undefined,
    parse,
)
from graphql.execution.base import (
    ExecutionContext,
    collect_fields,
    get_field_def,
    get_operation_root_type,
)
from graphql.pyutils.default_ordered_dict import DefaultOrderedDict


class DBStatementCounter(object):
    """
    Use as a context manager to count the number of execute()'s performed
    against the given sqlalchemy connection.

    Usage:
        with DBStatementCounter(conn) as ctr:
            conn.execute("SELECT 1")
            conn.execute("SELECT 1")
        assert ctr.get_count() == 2
    """
    def __init__(self, conn):
        self.conn = conn
        self.count = 0
        # Will have to rely on this since sqlalchemy 0.8 does not support
        # removing event listeners
        self.do_count = False
        sqlalchemy.event.listen(conn, 'after_execute', self.callback)

    def __enter__(self):
        self.do_count = True
        return self

    def __exit__(self, *_):
        self.do_count = False

    def get_count(self):
        return self.count

    def callback(self, *_):
        if self.do_count:
            self.count += 1
def create_execution_context(schema, request_string):
    source = Source(request_string, 'GraphQL request')
    document_ast = parse(source)
    return ExecutionContext(
        schema,
        document_ast,
        root_value=None,
        context_value=None,
        variable_values=None,
        operation_name=None,
        executor=None,
        middleware=None,
        allow_subscriptions=False,
    )


def get_field_asts_from_execution_context(exe_context):
    fields = collect_fields(
        exe_context,
        type,
        exe_context.operation.selection_set,
        DefaultOrderedDict(list),
        set()
    )
    # field_asts = next(iter(fields.values()))
    field_asts = tuple(fields.values())[0]
    return field_asts

def create_resolve_info(schema, request_string):
    exe_context = create_execution_context(schema, request_string)
    parent_type = get_operation_root_type(schema, exe_context.operation)
    field_asts = get_field_asts_from_execution_context(exe_context)

    field_ast = field_asts[0]
    field_name = field_ast.name.value

    field_def = get_field_def(schema, parent_type, field_name)
    if not field_def:
        return Undefined
    return_type = field_def.type

    # The resolve function's optional third argument is a context value that
    # is provided to every resolve function within an execution. It is commonly
    # used to represent an authenticated user, or request-specific caches.
    context = exe_context.context_value
    return ResolveInfo(
        field_name,
        field_asts,
        return_type,
        parent_type,
        schema=schema,
        fragments=exe_context.fragments,
        root_value=exe_context.root_value,
        operation=exe_context.operation,
        variable_values=exe_context.variable_values,
        context=context
    )


def get_query(statment):
    return statment.compile(compile_kwargs={"literal_binds": True})