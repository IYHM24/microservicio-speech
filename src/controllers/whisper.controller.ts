import type { Request, Response } from 'express';
import { logger } from '../config/constantes.js';

export const voiceToText = (req: Request, res: Response) => {
    logger.info('Realizando la conversion de voz a texto');
}