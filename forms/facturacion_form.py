"""
Formulario del módulo de facturación.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):
    numero = StringField(
        "Número de factura",
        validators=[
            DataRequired(message="El número de factura es obligatorio."),
            Length(min=9, max=17, message="Use el formato 001-001-000129.")
        ]
    )

    fecha = DateField(
        "Fecha de emisión",
        format="%Y-%m-%d",
        validators=[DataRequired(message="La fecha es obligatoria.")]
    )

    # Las opciones de clientes se cargan desde app.py al crear el formulario
    cliente = SelectField(
        "Cliente",
        choices=[],
        validators=[DataRequired(message="Debe seleccionar un cliente.")]
    )

    total = FloatField(
        "Total de la factura ($)",
        validators=[
            DataRequired(message="El total es obligatorio."),
            NumberRange(min=0.01, message="El total debe ser mayor a $0.00.")
        ]
    )

    estado = SelectField(
        "Estado de la factura",
        choices=[
            ("", "-- Seleccione el estado --"),
            ("Pagada", "Pagada"),
            ("Pendiente", "Pendiente")
        ],
        validators=[DataRequired(message="Debe seleccionar el estado.")]
    )

    submit = SubmitField("Guardar factura")
