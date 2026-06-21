import logging
import structlog
import sys


def setup_logger():
    processors =  [   #processorlar burada işlenecek.

    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.JSONRenderer()

    ]
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,

    )
    
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,

    )



if __name__ == "__main__":
    setup_logger()
    logger = structlog.get_logger("benim_uygulamam")
    logger.info("kullanici_kayit_oldu", kullanici_adi="yigit", durum="basarili", deneme_sayisi=1)

