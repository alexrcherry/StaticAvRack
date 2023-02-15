import nidaqmx as ni
from nidaqmx.stream_readers import AnalogMultiChannelReader

def sys_init():
    #init nidaq system
    sys = ni.system.System.local()

    #define devices as currently configured in AvRack
    ni_chassis_dev = sys.devices['cDAQ1'] #8 slot NI CompactDAQ 9178 Device
    ni_9237_dev = sys.devices['cDAQ1Mod4'] #bridge analog input module 9237 on slot 4 of chassis
    ni_9485_1_dev = sys.devices['cDAQ1Mod5'] #ssr voltage output module 9485 on slot 5 of chassis
    ni_9485_2_dev = sys.devices['cDAQ1Mod6'] #ssr voltage output module 9485 on slot 6 of chassis
    ni_9205_dev = sys.devices['cDAQ1Mod7'] #voltage input module 9205 on slot 7 of chassis
    ni_9213_dev = sys.devices['cDAQMod8'] #temperature input module 9213 on slot 8 of chassis
    
    return sys

def ai_task_init(sys):

    ni_9205_dev = sys.devices['cDAQ1Mod7']
    ai_read_task = ni.Task()
    ai_read_task.ai_channels.add_ai_voltage_chan(ni_9205_dev.name+'/ai0:5', terminal_config=ni.constants.TerminalConfiguration.RSE, min_val=1.996, max_val=9.980)
    ai_read_task.timing.cfg_samp_clk_timing(1000, source="", sample_mode=ni.constants.AcquisitionType.CONTINUOUS)
    ai_reader = AnalogMultiChannelReader(ai_read_task.in_stream)
    ai_read_task.start()

    return [ai_reader, ai_read_task]

def do_tasks_init(sys):

    ni_9485_1_dev = sys.devices['cDAQ1Mod5']
    ni_9485_2_dev = sys.devices['cDAQ1Mod6']

    do_write_task_0 = ni.Task()
    do_write_task_1 = ni.Task()
    do_write_task_2 = ni.Task()
    do_write_task_3 = ni.Task()
    do_write_task_4 = ni.Task()
    do_write_task_5 = ni.Task()
    do_write_task_6 = ni.Task()
    do_write_task_7 = ni.Task()

    do_write_task_8 = ni.Task()
    
    #need to add each virtual channel individually so the lines for each solenoid are not grouped together (?)
    do_write_task_0.do_channels.add_do_chan(ni_9485_1_dev.name+'/port0/line0', line_grouping=ni.constants.LineGrouping.CHAN_PER_LINE)
    do_write_task_1.do_channels.add_do_chan(ni_9485_1_dev.name+'/port0/line1', line_grouping=ni.constants.LineGrouping.CHAN_PER_LINE)
    do_write_task_2.do_channels.add_do_chan(ni_9485_1_dev.name+'/port0/line2', line_grouping=ni.constants.LineGrouping.CHAN_PER_LINE)
    do_write_task_3.do_channels.add_do_chan(ni_9485_1_dev.name+'/port0/line3', line_grouping=ni.constants.LineGrouping.CHAN_PER_LINE)
    do_write_task_4.do_channels.add_do_chan(ni_9485_1_dev.name+'/port0/line4', line_grouping=ni.constants.LineGrouping.CHAN_PER_LINE)
    do_write_task_5.do_channels.add_do_chan(ni_9485_1_dev.name+'/port0/line5', line_grouping=ni.constants.LineGrouping.CHAN_PER_LINE)
    do_write_task_6.do_channels.add_do_chan(ni_9485_1_dev.name+'/port0/line6', line_grouping=ni.constants.LineGrouping.CHAN_PER_LINE)
    do_write_task_7.do_channels.add_do_chan(ni_9485_1_dev.name+'/port0/line7', line_grouping=ni.constants.LineGrouping.CHAN_PER_LINE)

    do_write_task_8.do_channels.add_do_chan(ni_9485_2_dev.name+'/port0/line4', line_grouping=ni.constants.LineGrouping.CHAN_PER_LINE)

    return [do_write_task_0, do_write_task_1, do_write_task_2, do_write_task_3, do_write_task_4, do_write_task_5, do_write_task_6, do_write_task_7, do_write_task_8]
