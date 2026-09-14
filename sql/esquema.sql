-- ============================================================
-- esquema.sql - Base de datos de JM Ferretería
-- Ejecutar este archivo para crear la base y sus tablas.
-- ============================================================

CREATE DATABASE IF NOT EXISTS jm_ferreteria
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE jm_ferreteria;


-- ------------------------------------------------------------
-- Tabla de proveedores
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    ruc VARCHAR(13) NOT NULL,
    empresa VARCHAR(80) NOT NULL,
    producto VARCHAR(60) NOT NULL,
    contacto VARCHAR(60) NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    correo VARCHAR(80),
    convenio TINYINT(1) NOT NULL DEFAULT 0
);


-- ------------------------------------------------------------
-- Tabla de clientes
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(13) NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    correo VARCHAR(80),
    ciudad VARCHAR(50) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1
);


-- ------------------------------------------------------------
-- Tabla de productos
-- Se relaciona con proveedores mediante la clave foránea id_proveedor
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    nombre VARCHAR(80) NOT NULL,
    categoria VARCHAR(30) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    precio DECIMAL(10,2) NOT NULL,
    id_proveedor INT,
    CONSTRAINT fk_producto_proveedor
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedores (id_proveedor)
        ON DELETE SET NULL
);


-- ------------------------------------------------------------
-- Tabla de facturas
-- Se relaciona con clientes mediante la clave foránea id_cliente
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL,
    id_cliente INT,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(15) NOT NULL,
    CONSTRAINT fk_factura_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes (id_cliente)
        ON DELETE SET NULL
);


-- ============================================================
-- Datos de ejemplo
-- ============================================================

INSERT INTO proveedores (ruc, empresa, producto, contacto, telefono, correo, convenio) VALUES
('1790012345001', 'Holcim Ecuador', 'Cemento', 'Ing. Pedro Salas', '023456789', 'ventas@holcim.ec', 1),
('1790067890001', 'Adelca', 'Hierro y varillas', 'Sra. Ana Lema', '023987654', 'ventas@adelca.ec', 1),
('1790054321001', 'Plastigama', 'Tuberías y accesorios', 'Ing. Jorge Vaca', '024567890', 'ventas@plastigama.ec', 0),
('1790098765001', 'Intaco Ecuador', 'Bondex y acabados', 'Sr. Diego Cruz', '025678901', 'ventas@intaco.ec', 1);

INSERT INTO clientes (cedula, nombre, telefono, correo, ciudad, tipo, activo) VALUES
('1719283746', 'Rosa Simbaña', '0991234567', 'rosa.simbana@gmail.com', 'Quito', 'Frecuente', 1),
('1712345678', 'Luis Guamán', '0987654321', 'luis.guaman@gmail.com', 'Calderón', 'Mayorista', 1),
('1798765432', 'Constructora Andina S.A.', '022345678', 'info@andina.ec', 'Quito', 'Empresa', 1),
('1701122334', 'Marco Tipán', '0962959355', '', 'Carapungo', 'Ocasional', 0);

INSERT INTO productos (codigo, nombre, categoria, stock, precio, id_proveedor) VALUES
('P001', 'Cemento Selvalegre 50 kg', 'Cemento', 120, 8.50, 1),
('P002', 'Bloque de 15 cm', 'Bloques', 850, 0.65, NULL),
('P003', 'Varilla de hierro 12 mm', 'Hierro', 240, 12.30, 2),
('P004', 'Malla Armex R-84', 'Hierro', 45, 28.90, 2),
('P005', 'Tubería Plastigama 110 mm', 'Tuberías', 0, 18.75, 3),
('P006', 'Bondex Intaco 25 kg', 'Acabados', 75, 9.40, 4),
('P007', 'Metro cúbico de ripio', 'Áridos', 30, 22.00, NULL),
('P008', 'Polvo azul (saco)', 'Áridos', 0, 6.80, NULL);

INSERT INTO facturas (numero, fecha, id_cliente, total, estado) VALUES
('001-001-000125', '2026-08-02', 1, 245.80, 'Pagada'),
('001-001-000126', '2026-08-05', 2, 480.00, 'Pendiente'),
('001-001-000127', '2026-08-08', 3, 1320.50, 'Pagada'),
('001-001-000128', '2026-08-12', 4, 96.25, 'Pendiente');
