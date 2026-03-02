import { LOG_LEVEL } from '../../config/constantes.js';
import { createLogger, format, transports } from 'winston';

// Formato personalizado con colores y timestamp
const customFormat = format.printf(({ level, message, timestamp, ...metadata }) => {
  const meta = Object.keys(metadata).length ? JSON.stringify(metadata, null, 2) : '';
  return `${timestamp} [${level}]: ${message} ${meta}`;
});

const logger = createLogger({
  level: LOG_LEVEL,
  format: format.combine(
    format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    format.errors({ stack: true }),
    format.splat(),
    format.colorize(),
    customFormat
  ),
  transports: [
    new transports.Console()
  ],
});

export default logger;