"""
Formulario del módulo de proveedores.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional


class ProveedorForm(FlaskForm):
    ruc = StringField(
        "RUC de la empresa",
        validators=[
            DataRequired(message="El RUC es obligatorio."),
            Length(min=13, max=13, message="El RUC debe tener exactamente 13 dígitos.")
        ]
    )

    empresa = StringField(
        "Nombre de la empresa",
        validators=[
            DataRequired(message="El nombre de la empresa es obligatorio."),
            Length(min=3, max=80, message="El nombre debe tener entre 3 y 80 caracteres.")
        ]
    )

    producto = StringField(
        "Producto que provee",
        validators=[
            DataRequired(message="Debe indicar qué producto provee."),
            Length(min=3, max=60, message="Debe tener entre 3 y 60 caracteres.")
        ]
    )

    contacto = StringField(
        "Persona de contacto",
        validators=[
            DataRequired(message="El nombre del contacto es obligatorio."),
            Length(min=3, max=60, message="Debe tener entre 3 y 60 caracteres.")
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(min=7, max=10, message="El teléfono debe tener entre 7 y 10 dígitos.")
        ]
    )

    correo = StringField(
        "Correo electrónico (opcional)",
        validators=[
            Optional(),
            Email(message="Ingrese un correo electrónico válido.")
        ]
    )

    convenio = BooleanField("Tiene convenio vigente")

    submit = SubmitField("Guardar proveedor")
