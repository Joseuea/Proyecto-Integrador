"""
Formulario del módulo de productos.
La misma clase sirve para registrar y para editar un producto.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):
    codigo = StringField(
        "Código del producto",
        validators=[
            DataRequired(message="El código es obligatorio."),
            Length(min=4, max=10, message="El código debe tener entre 4 y 10 caracteres.")
        ]
    )

    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=80, message="El nombre debe tener entre 3 y 80 caracteres.")
        ]
    )

    categoria = SelectField(
        "Categoría",
        choices=[
            ("", "-- Seleccione una categoría --"),
            ("Cemento", "Cemento"),
            ("Bloques", "Bloques"),
            ("Hierro", "Hierro"),
            ("Tuberías", "Tuberías"),
            ("Acabados", "Acabados"),
            ("Áridos", "Áridos")
        ],
        validators=[DataRequired(message="Debe seleccionar una categoría.")]
    )

    stock = IntegerField(
        "Stock disponible",
        validators=[
            DataRequired(message="El stock es obligatorio."),
            NumberRange(min=0, max=10000, message="El stock debe estar entre 0 y 10000 unidades.")
        ]
    )

    precio = FloatField(
        "Precio unitario ($)",
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(min=0.01, max=5000, message="El precio debe estar entre $0.01 y $5000.")
        ]
    )

    submit = SubmitField("Guardar producto")
