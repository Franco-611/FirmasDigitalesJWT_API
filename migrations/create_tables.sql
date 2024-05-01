CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL NOT NULL,
    public_key TEXT NOT NULL,
    username VARCHAR(30) NOT NULL UNIQUE,
    fecha_creacion TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);

