import sys
from do_job_utils import Config, parse_args
from job_func import exam_standard_job_func


job_maps = {
    'exam_standard': exam_standard_job_func
}


def do_job(cfg):
    pipeline = cfg.cfgMap['job']["pipeline"]
    jobs = cfg.cfgMap['job'][pipeline].split(',')

    for job in jobs:
        print('{} starting ....'.format(job))
        job_cfg = cfg.cfgMap[job]
        job_maps[job](job_cfg)
        print('{} finished'.format(job))

    return


def main():
    ret, err_msg, options, args = parse_args()

    if ret != 0:
        print(err_msg)
        sys.exit(-1)

    cfg = Config(options.configFile)
    cfg.parse()
    print(cfg.cfgMap)

    do_job(cfg)

    return


if __name__ == '__main__':
    main()
