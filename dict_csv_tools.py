def public(mydict):
    return_me = {}
    for k, v in mydict.items():
        if str(k)[0] == "_":
            continue
        return_me[k] = v
    return return_me
