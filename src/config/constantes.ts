import dotenv from 'dotenv';
import app from './express.js';
import LoggerClass from '../components/logger/logger.js'

dotenv.config();

//Logger
export const logger = LoggerClass;

//Express - Conexion de la app 
export const appExpress = app;
