from bwa_aligner.logger import Logger
from bwa_aligner.config import Config
from bwa_aligner.core import BwaAligner

logger = Logger()

try:
    BwaAligner(
        config=Config("/data/config.json"),
        output_dir_path="/data/out/files",
        logger=logger
    ).run()
except Exception as e:
    logger.log_error(str(e))
