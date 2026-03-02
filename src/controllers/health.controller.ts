import type { Request, Response } from 'express';
import { logger } from '../config/constantes.js';

export const getHealth = (req: Request, res: Response) => {
    logger.info('Health check requested');
    return res.json({ message: 'API funcionando 🚀', uptime: process.uptime() });
}