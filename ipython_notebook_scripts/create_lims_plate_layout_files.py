import os # operating system specifics for paths
import json # json file library
import random # random numbers
import time # date and time
import sys # system exit
from pprint import pprint # pretty print 

# *****************************************************************************
# vvvvvvvvvvvvvvvvvvvvvvvv CHANGE THE LINES BELOW ONLY vvvvvvvvvvvvvvvvvvvvvvvv

lims_plate_grouping_id    = '10000001'          # must be unique id for this group of plates in single quotes. ALWAYS CHANGE THIS!
number_plates             = 3                   # max is 16, no quotes. ALWAYS CHECK THIS!
standards_type            = 'SS2'               # type of standards plate to be used (the standards config file to use)
library_prep_type         = 'SS2'               # type of library prep to do (the library prep config file to use)
number_wells_per_plate    = 384                 # should be no reason to change this as DNA quant is for 384-well plates
has_control_wells         = True                # True or False. If False then the 'plate_control_layout' field below is not used. ALWAYS CHECK THIS!
plate_control_layout      = 'controls_384'      # 'controls_384' or 'controls_4_x_96' or whatever, matching 'control_layouts' below. ALWAYS CHECK THIS!

# plate barcodes are enclosed by single quotes. ALWAYS CHANGE THESE! you only need to have as many as 'number_plates' above.
plate_barcodes = [
'SCG::00000001',
'SCG::00000002',
'SCG::00000003',
'SCG::00000004',
'SCG::00000005',
'SCG::00000006',
'SCG::00000007',
'SCG::00000008',
'SCG::00000009',
'SCG::00000010',
'SCG::00000011',
'SCG::00000012',
'SCG::00000013',
'SCG::00000014',
'SCG::00000015',
'SCG::00000016'
]

# control well types and locations
control_layouts = {
    'controls_384' : {
        '50_cell_with_LB'         : ['A1'],
        'positive_RNA_with_LB'    : ['P21'],
        'negative_no_RNA_with_LB' : ['P22'],
        'positive_RNA_qc_LB'      : ['P23'],
        'negative_no_RNA_qc_LB'   : ['P24']
    },
    'controls_4_x_96' : {
        '50_cell_with_LB'         : ['A1','A2','B1','B2'],
        'positive_RNA_with_LB'    : ['O17','O18','P17','P18'],
        'negative_no_RNA_with_LB' : ['O19','O20','P19','P20'],
        'positive_RNA_qc_LB'      : ['O21','O22','P21','P22'],
        'negative_no_RNA_qc_LB'   : ['O23','O24','P23','P24']
    }
}

# ^^^^^^^^^^^^^^^^^^^^^^^^^^ CHANGE THE LINES ABOVE ONLY ^^^^^^^^^^^^^^^^^^^^^^
# *****************************************************************************
def generate_barcode(prefix, counter):
    '''Generate a barcodes'''
    
    return prefix + str(1000000 + counter)

def generate_well_position_rows_then_columns(counter):
    '''Use this one if you want results ordered as A1, B1, C1, etc.'''
    
    i_row           = counter % 16
    i_col           = (counter - 1)/16
    s_well_posn     = row_list[(i_row - 1)] + str(i_col + 1)

    return s_well_posn

def generate_well_position_columns_then_rows(counter):
    '''Use this one if you want results ordered as A1, A2, A3, etc.'''

#     print("counter = %s" % counter)
    i_row = (counter - 1)/24
#     print("i_row = %s" % str(i_row))
    i_col = (counter - 1) % 24
#     print("i_col = %s" % str(i_col))
    s_well_posn = row_list[i_row] + str(i_col + 1)
#     print("s_well_posn = %s" % s_well_posn)
#     print("-" * 50)

    return s_well_posn

def well_position_already_exists(well_position, wells_dict):
    '''Check if this position has already been used for a control'''
    
    for w in wells_dict:
        if(w["POSITION"] == well_position):
            return True
    return False

print("Starting")

row_list          = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P"]

# filedir         = 'C:\\as28\\network' # note the double-slashes in the path and must be in single quotes
filedir           = '/Users/as28/Documents/PYTHON/team214/network/'

s_ts              = time.strftime("%Y%m%d_%H%M%S_")
filename          = s_ts + lims_plate_grouping_id + '.json' # prefixed with timestamp and filetype JSON
filepath          = os.path.join(filedir, filename)

data              = {"LIMS_PLATE_GROUP_ID":str(lims_plate_grouping_id), "PLATES" : {}}

well_id_counter   = 1
plate_counter     = 1

# generate the plate data
while plate_counter <= number_plates:

    # print("plate : %s out of %s" % (plate_counter, number_plates))

    s_plt_cnt                               = str(plate_counter)
    curr_plate_data                         = {}
    
    # fetch plate barcode from list
    barcode                                 = plate_barcodes[plate_counter -1]
    
    # set plate parameters
    curr_plate_data["BARCODE"]              = barcode
    curr_plate_data["LIBRARY_PREP_PARAMS"]  = library_prep_type
    curr_plate_data["STANDARDS_PARAMS"]     = standards_type
    
    # generate wells data
    wells_data                              = []
    well_counter                            = 1 # well num in this plate 1-384
    sample_counter                          = 1 # sample num in this plate
    control_counter                         = 1 # control num in this plate
    
    # print("checking for control wells")

    # add control wells
    if(has_control_wells):
        # print("has control wells")
        if(not plate_control_layout in control_layouts):
            # print("ERROR: plate_control_layout <%s> not recognised as a control_layout" % plate_control_layout)
            sys.exit()
        else:
            # print("matched control layout")
            controls_dict = control_layouts[plate_control_layout]

            # print("controls dict:")
            # pprint(controls_dict)

            for s_control_type, well_locns_list in controls_dict.iteritems():

                # print("s_control_type = %s" % s_control_type)
                # print("well_locns_list:")
                # pprint(well_locns_list)

                for s_well_locn in well_locns_list:

                    # print("s_well_locn : %s" % s_well_locn)

                    well_data                   = {}
            
                    # set wells parameters
                    well_data["POSITION"]       = s_well_locn
                    well_data["ID"]             = generate_barcode("W", well_id_counter)
                    well_data["ROLE"]           = "CONTROL"
                    well_data["SAMPLE_TYPE"]    = s_control_type

                    # print("well data: ")
                    # pprint(well_data)
                                       
                    wells_data.append(well_data)       

                    # increment well counters
                    control_counter             += 1
                    well_id_counter             += 1

    # now fill in the remainder of the plate with sample wells
    while well_counter <= number_wells_per_plate:

        # print("well_counter = %s" % well_counter)
        
        # generate well position
        current_well_position       = generate_well_position_columns_then_rows(well_counter)

        # print("current_well_position = %s" % current_well_position)

        # check if this position has already been used for a control
        if(not well_position_already_exists(current_well_position, wells_data)):

            # print("adding sample at posn = %s" % current_well_position)

            well_data                   = {}
            
            # ser wells parameters
            well_data["POSITION"]       = current_well_position
            well_data["ID"]             = generate_barcode("W", well_id_counter)
            well_data["ROLE"]           = "SAMPLE"
            well_data["SAMPLE_TYPE"]    = "cDNAclean"
            
            wells_data.append(well_data)       

            # increment sample counters
            sample_counter              += 1
        
        # increment well counters
        well_counter                += 1
        well_id_counter             += 1

    # add wells data to plate
    curr_plate_data["WELLS"]    = wells_data
    
    # add plate to main dictionary
    data["PLATES"][s_plt_cnt]   = curr_plate_data
    
    # increment plate counter
    plate_counter               += 1

# write the data to the file   
with open(filepath, 'w') as outfile:
    json.dump(data, outfile)

# display filepath of the file
print("File created at : %s" % filepath)
pprint(data)