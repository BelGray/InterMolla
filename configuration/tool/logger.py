from BGLogger import *
log = Log(process_name='InterMolla Live Cycle', record=False, return_every_log=False, output_style=OutputStyle.BOLD, color=True)
log.set_log_line_template(f'[InterMolla * %L]\nTAG: %T\nMESSAGE: %M\nDATE: %D')