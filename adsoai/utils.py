import json
import os
from datetime import date, datetime
from pathlib import Path

class GetLastHarvestException(Exception):
    pass


class LoadSetListException(Exception):
    pass


class LogHarvestException(Exception):
    pass


class MakeFilepathException(Exception):
    pass


class WriteDataCiteException(Exception):
    pass


def load_setlist(sets_file=None):
    setlist = []
    try:
        if not sets_file:
            raise Exception("You must supply a valid filename.")
        else:
            if not os.path.exists(sets_file):
                raise Exception("The specified sets file does not exist.")
            else:
                try:
                    with open(sets_file, "r") as fs:
                        for line in fs.readlines():
                            columns = line.strip().split('#')
                            setuser = columns[0].strip()
                            if setuser:
                                setlist.append(setuser)
                except Exception as err:
                    raise Exception("Error reading sets file: %s" % err)
    except Exception as err:
        raise LoadSetListException("Error: %s" % err)
    else:
        return setlist


def get_last_harvest(log_dir=None, setuser=None):
    try:
        if log_dir and setuser:
            logfilename = log_dir + "/" + setuser + "_harvest_log.json"
            if not os.path.exists(logfilename):
                return
            else:
                with open(logfilename, "r") as fj:
                    setlog = json.load(fj)
                logs = setlog.get("harvests", [])
                last_log = logs[-1]
                last_start_time = last_log.get("timestart", None)
                if not last_start_time:
                    return
                else:
                    last_date = date.isoformat(datetime.fromisoformat(last_start_time))
                    return last_date
        else:
            raise Exception("You must supply both a logging directory and a set name.")
    except Exception as err:
        raise GetLastHarvestException("Error: %s" % err)

def log_harvest(log_dir=None, setuser=None, log_record={}):
    try:
        if log_dir and setuser and log_record:
            logfilename = log_dir + "/" + setuser + "_harvest_log.json"
            if not os.path.exists(log_dir):
                Path(log_dir).mkdir(parents=True, exist_ok=True)
          
            if os.path.exists(logfilename):
                with open(logfilename, "r") as fj:
                    setlog = json.load(fj)
                logs = setlog.get("harvests", [])
            else:
                logs = []
            logs.append(log_record)
            new_setlog = {"harvests": logs}
            with open(logfilename, "w") as fj:
                fj.write(json.dumps(new_setlog, indent=2))
        else:
            raise Exception("Unable to log current harvest.")
    except Exception as err:
        raise LogHarvestException("Error: %s" % err)

def write_zenodo_record(archive_dir=None, record=None):
    try:
        outpath = make_zenodo_filepath(archive_dir, record)
        Path(outpath).mkdir(parents=True, exist_ok=True)
        outfile = os.path.normpath(outpath + "/metadata.xml")
        with open(outfile, "w") as fout:
            fout.write("%s" % record)
        return outfile
    except Exception as err:
        raise WriteDataCiteException("Error: %s" % err)

def make_zenodo_filepath(archive_dir=None, record=None):
    try:
        ident = record.metadata.get("alternateIdentifier", None)
        if not ident:
            raise Exception("Identifier not found in record.")
        else:
            idstring = ident[0]
            (prefix, uri, record_id) = idstring.split(":")
            pathlist = [prefix, uri]
            while record_id:
                pathlist.append(record_id[0:2])
                if len(record_id) > 2:
                    record_id = record_id[2:]
                else:
                    record_id = None
            return os.path.normpath(archive_dir + "/" + ("/".join(pathlist)))
    except Exception as err:
        raise MakeFilepathException("Unable to create a pathname for record output: %s" % err)
