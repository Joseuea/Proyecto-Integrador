"""
Formulario para registrar usuarios del sistema.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class UsuarioForm(FlaskForm):
    usuario = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(message="El nombre de usuario es obligatorio."),
            Length(min=3, max=50, message="El usuario debe tener entre 3 y 50 caracteres.")
        ]
    )

    nombre = StringField(
        "Nombre completo",
        validators=[
            DataRequired(message="El nombre completo es obligatorio."),
            Length(min=3, max=80, message="El nombre debe tener entre 3 y 80 caracteres.")
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")
        ]
    )

    # EqualTo compara este campo con el anterior para evitar errores al escribir
    confirmar = PasswordField(
        "Repita la contraseña",
        validators=[
            DataRequired(message="Debe repetir la contraseña."),
            EqualTo("password", message="Las contraseñas no coinciden.")
        ]
    )

    submit = SubmitField("Registrar usuario")
