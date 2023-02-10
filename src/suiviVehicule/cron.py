from suiviVehicule.services import services
import logging
logger = logging.getLogger(__name__)

def test():
    services().gestion_status_pos()
    logger.info("CALL")