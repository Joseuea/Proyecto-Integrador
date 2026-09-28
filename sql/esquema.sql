-- ============================================================
-- esquema.sql - Base de datos de JM Ferretería (PostgreSQL)
-- Ejecutar este archivo para crear las tablas del sistema.
--
-- En local:   psql -U postgres -d jm_ferreteria -f sql/esquema.sql
-- En Render:  copiar y pegar el contenido en la consola de la base.
-- ============================================================


-- ------------------------------------------------------------
-- Tabla de usuarios del sistema
-- La contraseña nunca se guarda en texto plano: se almacena
-- el hash generado con generate_password_hash().
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    password VARCHAR(255) NOT NULL
);


-- ------------------------------------------------------------
-- Tabla de proveedores
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    ruc VARCHAR(13) NOT NULL,
    empresa VARCHAR(80) NOT NULL,
    producto VARCHAR(60) NOT NULL,
    contacto VARCHAR(60) NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    correo VARCHAR(80),
    convenio BOOLEAN NOT NULL DEFAULT FALSE
);


-- ------------------------------------------------------------
-- Tabla de clientes
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    cedula VARCHAR(13) NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    correo VARCHAR(80),
    ciudad VARCHAR(50) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);


-- ------------------------------------------------------------
-- Tabla de productos
-- Relacionada con proveedores mediante la clave foránea id_proveedor
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    nombre VARCHAR(80) NOT NULL,
    categoria VARCHAR(30) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    precio NUMERIC(10,2) NOT NULL,
    id_proveedor INTEGER,
    CONSTRAINT fk_producto_proveedor
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedores (id_proveedor)
        ON DELETE SET NULL
);


-- ------------------------------------------------------------
-- Tabla de facturas
-- Relacionada con clientes mediante la clave foránea id_cliente
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    numero VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL,
    id_cliente INTEGER,
    total NUMERIC(10,2) NOT NULL,
    estado VARCHAR(15) NOT NULL,
    CONSTRAINT fk_factura_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes (id_cliente)
        ON DELETE SET NULL
);


-- ============================================================
-- Datos de ejemplo
-- Solo se insertan si las tablas están vacías, para no duplicar
-- registros cada vez que se ejecuta el archivo.
-- ============================================================

INSERT INTO proveedores (ruc, empresa, producto, contacto, telefono, correo, convenio)
SELECT * FROM (VALUES
    ('1790012345001', 'Holcim Ecuador', 'Cemento', 'Ing. Pedro Salas', '023456789', 'ventas@holcim.ec', TRUE),
    ('1790067890001', 'Adelca', 'Hierro y varillas', 'Sra. Ana Lema', '023987654', 'ventas@adelca.ec', TRUE),
    ('1790054321001', 'Plastigama', 'Tuberías y accesorios', 'Ing. Jorge Vaca', '024567890', 'ventas@plastigama.ec', FALSE),
    ('1790098765001', 'Intaco Ecuador', 'Bondex y acabados', 'Sr. Diego Cruz', '025678901', 'ventas@intaco.ec', TRUE)
) AS nuevos
WHERE NOT EXISTS (SELECT 1 FROM proveedores);

INSERT INTO clientes (cedula, nombre, telefono, correo, ciudad, tipo, activo)
SELECT * FROM (VALUES
    ('1719283746', 'Rosa Simbaña', '0991234567', 'rosa.simbana@gmail.com', 'Quito', 'Frecuente', TRUE),
    ('1712345678', 'Luis Guamán', '0987654321', 'luis.guaman@gmail.com', 'Calderón', 'Mayorista', TRUE),
    ('1798765432', 'Constructora Andina S.A.', '022345678', 'info@andina.ec', 'Quito', 'Empresa', TRUE),
    ('1701122334', 'Marco Tipán', '0962959355', '', 'Carapungo', 'Ocasional', FALSE)
) AS nuevos
WHERE NOT EXISTS (SELECT 1 FROM clientes);

INSERT INTO productos (codigo, nombre, categoria, stock, precio, id_proveedor)
SELECT * FROM (VALUES
    ('P001', 'Cemento Selvalegre 50 kg', 'Cemento', 120, 8.50, 1),
    ('P002', 'Bloque de 15 cm', 'Bloques', 850, 0.65, NULL),
    ('P003', 'Varilla de hierro 12 mm', 'Hierro', 240, 12.30, 2),
    ('P004', 'Malla Armex R-84', 'Hierro', 45, 28.90, 2),
    ('P005', 'Tubería Plastigama 110 mm', 'Tuberías', 0, 18.75, 3),
    ('P006', 'Bondex Intaco 25 kg', 'Acabados', 75, 9.40, 4),
    ('P007', 'Metro cúbico de ripio', 'Áridos', 30, 22.00, NULL),
    ('P008', 'Polvo azul (saco)', 'Áridos', 0, 6.80, NULL)
) AS nuevos (codigo, nombre, categoria, stock, precio, id_proveedor)
WHERE NOT EXISTS (SELECT 1 FROM productos);

INSERT INTO facturas (numero, fecha, id_cliente, total, estado)
SELECT * FROM (VALUES
    ('001-001-000125', DATE '2026-08-02', 1, 245.80, 'Pagada'),
    ('001-001-000126', DATE '2026-08-05', 2, 480.00, 'Pendiente'),
    ('001-001-000127', DATE '2026-08-08', 3, 1320.50, 'Pagada'),
    ('001-001-000128', DATE '2026-08-12', 4, 96.25, 'Pendiente')
) AS nuevos
WHERE NOT EXISTS (SELECT 1 FROM facturas);
