-- ============================================================
-- esquema_sqlite.sql - Base de datos de JM Ferretería (SQLite)
--
-- Es la misma estructura del archivo esquema.sql, escrita con la
-- sintaxis de SQLite. La aplicación lo ejecuta sola al iniciarse
-- cuando trabaja en modo SQLite, así que no hace falta correrlo
-- a mano.
-- ============================================================


-- ------------------------------------------------------------
-- Tabla de usuarios del sistema
-- La contraseña nunca se guarda en texto plano: se almacena
-- el hash generado con generate_password_hash().
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    password TEXT NOT NULL
);


-- ------------------------------------------------------------
-- Tabla de proveedores
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
    ruc TEXT NOT NULL,
    empresa TEXT NOT NULL,
    producto TEXT NOT NULL,
    contacto TEXT NOT NULL,
    telefono TEXT NOT NULL,
    correo TEXT,
    convenio INTEGER NOT NULL DEFAULT 0
);


-- ------------------------------------------------------------
-- Tabla de clientes
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    cedula TEXT NOT NULL,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    correo TEXT,
    ciudad TEXT NOT NULL,
    tipo TEXT NOT NULL,
    activo INTEGER NOT NULL DEFAULT 1
);


-- ------------------------------------------------------------
-- Tabla de productos
-- Relacionada con proveedores mediante la clave foránea id_proveedor
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    precio REAL NOT NULL,
    id_proveedor INTEGER,
    FOREIGN KEY (id_proveedor)
        REFERENCES proveedores (id_proveedor)
        ON DELETE SET NULL
);


-- ------------------------------------------------------------
-- Tabla de facturas
-- Relacionada con clientes mediante la clave foránea id_cliente
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS facturas (
    id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT NOT NULL,
    fecha TEXT NOT NULL,
    id_cliente INTEGER,
    total REAL NOT NULL,
    estado TEXT NOT NULL,
    FOREIGN KEY (id_cliente)
        REFERENCES clientes (id_cliente)
        ON DELETE SET NULL
);


-- ============================================================
-- Datos de ejemplo
-- Solo se insertan la primera vez, para no duplicar registros
-- cada vez que se ejecuta la aplicación.
-- ============================================================

INSERT INTO proveedores (ruc, empresa, producto, contacto, telefono, correo, convenio)
SELECT '1790012345001', 'Holcim Ecuador', 'Cemento', 'Ing. Pedro Salas', '023456789', 'ventas@holcim.ec', 1
WHERE NOT EXISTS (SELECT 1 FROM proveedores);

INSERT INTO proveedores (ruc, empresa, producto, contacto, telefono, correo, convenio)
SELECT '1790067890001', 'Adelca', 'Hierro y varillas', 'Sra. Ana Lema', '023987654', 'ventas@adelca.ec', 1
WHERE (SELECT COUNT(*) FROM proveedores) = 1;

INSERT INTO proveedores (ruc, empresa, producto, contacto, telefono, correo, convenio)
SELECT '1790054321001', 'Plastigama', 'Tuberías y accesorios', 'Ing. Jorge Vaca', '024567890', 'ventas@plastigama.ec', 0
WHERE (SELECT COUNT(*) FROM proveedores) = 2;

INSERT INTO proveedores (ruc, empresa, producto, contacto, telefono, correo, convenio)
SELECT '1790098765001', 'Intaco Ecuador', 'Bondex y acabados', 'Sr. Diego Cruz', '025678901', 'ventas@intaco.ec', 1
WHERE (SELECT COUNT(*) FROM proveedores) = 3;


INSERT INTO clientes (cedula, nombre, telefono, correo, ciudad, tipo, activo)
SELECT '1719283746', 'Rosa Simbaña', '0991234567', 'rosa.simbana@gmail.com', 'Quito', 'Frecuente', 1
WHERE NOT EXISTS (SELECT 1 FROM clientes);

INSERT INTO clientes (cedula, nombre, telefono, correo, ciudad, tipo, activo)
SELECT '1712345678', 'Luis Guamán', '0987654321', 'luis.guaman@gmail.com', 'Calderón', 'Mayorista', 1
WHERE (SELECT COUNT(*) FROM clientes) = 1;

INSERT INTO clientes (cedula, nombre, telefono, correo, ciudad, tipo, activo)
SELECT '1798765432', 'Constructora Andina S.A.', '022345678', 'info@andina.ec', 'Quito', 'Empresa', 1
WHERE (SELECT COUNT(*) FROM clientes) = 2;

INSERT INTO clientes (cedula, nombre, telefono, correo, ciudad, tipo, activo)
SELECT '1701122334', 'Marco Tipán', '0962959355', '', 'Carapungo', 'Ocasional', 0
WHERE (SELECT COUNT(*) FROM clientes) = 3;


INSERT INTO productos (codigo, nombre, categoria, stock, precio, id_proveedor)
SELECT 'P001', 'Cemento Selvalegre 50 kg', 'Cemento', 120, 8.50, 1
WHERE NOT EXISTS (SELECT 1 FROM productos);

INSERT INTO productos (codigo, nombre, categoria, stock, precio, id_proveedor)
SELECT 'P002', 'Bloque de 15 cm', 'Bloques', 850, 0.65, NULL
WHERE (SELECT COUNT(*) FROM productos) = 1;

INSERT INTO productos (codigo, nombre, categoria, stock, precio, id_proveedor)
SELECT 'P003', 'Varilla de hierro 12 mm', 'Hierro', 240, 12.30, 2
WHERE (SELECT COUNT(*) FROM productos) = 2;

INSERT INTO productos (codigo, nombre, categoria, stock, precio, id_proveedor)
SELECT 'P004', 'Malla Armex R-84', 'Hierro', 45, 28.90, 2
WHERE (SELECT COUNT(*) FROM productos) = 3;

INSERT INTO productos (codigo, nombre, categoria, stock, precio, id_proveedor)
SELECT 'P005', 'Tubería Plastigama 110 mm', 'Tuberías', 0, 18.75, 3
WHERE (SELECT COUNT(*) FROM productos) = 4;

INSERT INTO productos (codigo, nombre, categoria, stock, precio, id_proveedor)
SELECT 'P006', 'Bondex Intaco 25 kg', 'Acabados', 75, 9.40, 4
WHERE (SELECT COUNT(*) FROM productos) = 5;

INSERT INTO productos (codigo, nombre, categoria, stock, precio, id_proveedor)
SELECT 'P007', 'Metro cúbico de ripio', 'Áridos', 30, 22.00, NULL
WHERE (SELECT COUNT(*) FROM productos) = 6;

INSERT INTO productos (codigo, nombre, categoria, stock, precio, id_proveedor)
SELECT 'P008', 'Polvo azul (saco)', 'Áridos', 0, 6.80, NULL
WHERE (SELECT COUNT(*) FROM productos) = 7;


INSERT INTO facturas (numero, fecha, id_cliente, total, estado)
SELECT '001-001-000125', '2026-08-02', 1, 245.80, 'Pagada'
WHERE NOT EXISTS (SELECT 1 FROM facturas);

INSERT INTO facturas (numero, fecha, id_cliente, total, estado)
SELECT '001-001-000126', '2026-08-05', 2, 480.00, 'Pendiente'
WHERE (SELECT COUNT(*) FROM facturas) = 1;

INSERT INTO facturas (numero, fecha, id_cliente, total, estado)
SELECT '001-001-000127', '2026-08-08', 3, 1320.50, 'Pagada'
WHERE (SELECT COUNT(*) FROM facturas) = 2;

INSERT INTO facturas (numero, fecha, id_cliente, total, estado)
SELECT '001-001-000128', '2026-08-12', 4, 96.25, 'Pendiente'
WHERE (SELECT COUNT(*) FROM facturas) = 3;
