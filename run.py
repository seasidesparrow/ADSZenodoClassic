import os
import logging
import re
from adsoai.utils import (
    load_setlist,
    write_zenodo_record,
    get_last_harvest,
    log_harvest
)
#from adsputils import load_config, setup_logging
from SciXPipelineUtils.utils import load_config
from adsoai.harvest import ZenodoHarvester
from datetime import datetime, tzinfo
from pathlib import Path
from time import sleep

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), "./"))
conf = load_config(proj_home=proj_home)
#logger = setup_logging("zenodo-harvester",
#                       proj_home=proj_home,
#                       level=conf.get("LOGGING_LEVEL", "INFO"),
#                       attach_stdout=conf.get("LOG_STDOUT", False))
logger = logging.getLogger("zenodo-harvester")


def do_harvest(setuser=None, log_dir=None, last_harvest=None):
    z = ZenodoHarvester()
    harvest_start = datetime.isoformat(datetime.now())
    count = 0
    output_logfile = os.path.normpath(log_dir + "/" + setuser + ".out")
    try:
        z.get_records(setname=setuser,
                      last_logtime=last_harvest)
    except Exception as err:
        logger.warning("Unable to harvest set %s: %s" % (setuser, err))
    else:
        if z.records:
            with open(output_logfile, "w") as fout:
                for r in z.records:
                    count += 1
                    outfile = write_zenodo_record(archive_dir=proj_home,
                                                  record=r)
                    write_time = datetime.isoformat(datetime.now())
                    fout.write("%s\t%s\n" % (outfile, write_time))
               
    harvest_finish = datetime.isoformat(datetime.now())
    log_result = {"from": last_harvest,
                  "nrecords": count,
                  "timestart": harvest_start,
                  "timefinish": harvest_finish,
                  "type": "ListRecords"}
    log_harvest(log_dir=log_dir,
                setuser=setuser,
                log_record=log_result)

def main():
    try:
        filename = os.path.join(proj_home, conf.get("SETS_FILENAME", None))
        setlist = load_setlist(filename)
    except Exception as err:
        logger.error("Unable to get setlist: %s" % err)
    else:
        if not setlist:
            logger.error("No sets in setlist!")
        else:
            for setuser in setlist:
                try:
                    log_dir = os.path.join(proj_home, conf.get("LOG_DIR", None))
                    last_harvest = get_last_harvest(log_dir=log_dir,
                                                    setuser=setuser)
                    if not last_harvest:
                        last_harvest="1970-01-01"
                except Exception as err:
                     logger.debug("Unable to determine last harvest time: %s" % err)
                try:
                    logger.info("Harvesting %s since %s" % (setuser, last_harvest))
                    do_harvest(setuser=setuser,
                               log_dir=log_dir,
                               last_harvest=last_harvest)
                except Exception as err:
                    logger.debug("Harvesting failed: %s" % err)

                sleep(conf.get("SLEEP_TIME", 5))


if __name__ == "__main__":
    main()
