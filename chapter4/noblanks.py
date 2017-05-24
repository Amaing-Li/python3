
def read_data(filename):
    lines = []
    fh = None  # file handle
    try:
        fh = open(filename,encoding="utf8")
        for line in fh:
            if line.strip():  # not blank line
                lines.append(line)
    except (IOError,OSError) as err:
    #  except EnvironmentError as err:
        print(err)
        return []
    finally:
        if fh is not None:
            fh.close()
    return lines