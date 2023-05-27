from pydantic import create_model
from tortoise.models import Model
from tortoise.fields.relational import ForeignKeyFieldInstance
import typing as t
from pydantic import BaseModel


class BaseConfig:
    arbitrary_types_allowed = True


first_ifnotnone = lambda ins, new_val: ins if ins is not None else new_val


get_model_optional_fields = lambda model_class: set(
    [k for k, v in model_class._meta.fields_map.items() if not v.required]
)


def _model_fields2schema(model_class, _include_, _exclude_, _optionals_):
    if _include_ and _exclude_:
        raise ValueError("cant set include and exclude at once")
    fields_definitions = dict()
    if isinstance(_optionals_, bool):
        if _optionals_ is False:
            _optionals_ = set()
        else:
            _optionals_ = set(model_class._meta.fields_map.keys())
    exclude, include, optionals = map(
        lambda a: first_ifnotnone(a[0], a[1]),
        (
            (_exclude_, {"deleted_at"}),
            (_include_, set()),
            (_optionals_, get_model_optional_fields(model_class)),
        ),
    )
    for k, v in model_class._meta.fields_map.items():
        is_excluded, isnot_included = k in exclude, k not in include and len(include)
        is_fk = isinstance(v, ForeignKeyFieldInstance)
        if is_excluded or isnot_included:
            continue
        key = (k + "_id") if is_fk else k
        fields_definitions[key] = (
            int if is_fk else v.field_type,
            ... if k not in optionals and not is_fk else None,
        )
    return fields_definitions


def model_fields2schema(model_class, _include_, _exclude_, custom_fields, _optionals_):
    fields_definitions = dict()
    if model_class is not None:
        fields_definitions = _model_fields2schema(
            model_class, _include_, _exclude_, _optionals_
        )
    fields_definitions.update(custom_fields)
    return fields_definitions


def model2schema(
    name: str,
    model_class: t.Type[Model],
    *,
    _exclude_: set = None,
    _include_: set = None,
    _optionals_: set = None,
    _base_: type = None,
    **custom_fields: t.Dict[str, t.Type[BaseModel]]
) -> t.Type[BaseModel]:
    """
    create schema from model.
    `id`, `created_at`, `deleted_at` are always exclude from model
        if you need them you have to add them in include
    """
    schema = model_fields2schema(
        model_class, _include_, _exclude_, custom_fields, _optionals_
    )
    if _base_ is None:
        schema["__config__"] = BaseConfig
    model = create_model(name, __base__=_base_, **schema)
    return model
