import logger from "./logger.config.js";


class LoggerClass {
    
    /**
     * Logger de tipo info
     * @param msj 
     * @param args 
     */
    info(msj: string, ...args: any[]) {
        logger.info(msj, ...args);
    }

    /**
     * Logger de tipo error
     * @param msj 
     * @param args 
     */
    error(msj: string, ...args: any[]) {
        logger.error(msj, ...args);
    }

    /**
     * Logger de tipo warn
     * @param msj 
     * @param args 
     */
    advertencia(msj: string, ...args: any[]) {
        logger.warn(msj, ...args);
    }

    /**
     * Logger de tipo debug
     * @param msj 
     * @param args 
     */
    debug(msj: string, ...args: any[]) {
        logger.debug(msj, ...args);
    }

    /**
     * Logger de tipo verbose
     * @param msj 
     * @param args 
     */
    verbose(msj: string, ...args: any[]) {
        logger.verbose(msj, ...args);
    }

}

export default new LoggerClass();