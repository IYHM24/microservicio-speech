import dotenv from 'dotenv';
dotenv.config();

// Configuración de Winston
export const LOG_LEVEL = process.env.LOG_LEVEL || 'info';

/// Configuración de la conexion 
export const PORT = process.env.PORT || 3000;