"""
Formulario del módulo de clientes.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional


class ClienteForm(FlaskForm):
    cedula = StringField(
        "Cédula o RUC",
        validators=[
            DataRequired(message="La cédula o RUC es obligatoria."),
            Length(min=10, max=13, message="La cédula debe tener 10 dígitos y el RUC 13.")
        ]
    )

    nombre = StringField(
        "Nombre completo",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=80, message="El nombre debe tener entre 3 y 80 caracteres.")
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

    ciudad = StringField(
        "Ciudad o sector",
        validators=[
            DataRequired(message="La ciudad es obligatoria."),
            Length(min=3, max=50, message="La ciudad debe tener entre 3 y 50 caracteres.")
        ]
    )

    tipo = SelectField(
        "Tipo de cliente",
        choices=[
            ("", "-- Seleccione el tipo --"),
            ("Frecuente", "Frecuente"),
            ("Mayorista", "Mayorista"),
            ("Empresa", "Empresa"),
            ("Ocasional", "Ocasional")
        ],
        validators=[DataRequired(message="Debe seleccionar el tipo de cliente.")]
    )

    activo = BooleanField("Cliente activo", default=True)

    submit = SubmitField("Guardar cliente")
