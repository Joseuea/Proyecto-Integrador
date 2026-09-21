"""
Paquete forms: agrupa las clases de formularios de cada módulo.
Así puedo importarlos desde app.py con una sola línea.
"""

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

__all__ = [
    "ProductoForm", "ClienteForm", "ProveedorForm", "FacturacionForm",
    "LoginForm", "UsuarioForm"
]
