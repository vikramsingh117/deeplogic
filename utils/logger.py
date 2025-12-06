import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s → %(message)s"
)

logger = logging.getLogger("sync")
