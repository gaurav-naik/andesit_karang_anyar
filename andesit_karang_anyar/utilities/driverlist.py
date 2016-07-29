import frappe
from frappe import _
from frappe.desk.reportview import get_match_cond


def load_drivers(vehicleno):
    """Loads Drivers list in `__onload`"""
    #Get Vehicle Drivers
    vddict = frappe.db.sql("SELECT vehicle_driver FROM `tabVehicle Driver` WHERE parent = '{vno}';".format(vno=vehicleno), as_dict=1)

    vdlist = map(lambda x: x['vehicle_driver'], vddict) #Returns values of dict as a list.

    #Load drivers from license nos.
    dl = frappe.get_all("Driver", fields=["*"], filters={"name" : ["in", vdlist]}, order_by="wb_driver_fn")
    return dl


# def load_drivers(vehicleno):
# 	"""Loads Drivers list in `__onload`"""

# 	# treiberen = frappe.get_all("Vehicle Driver", fields=['*'], filters={"parent": vehicleno}, order_by="driver_name")
# 	# return treiberen

# 	#Get Licence nos from Vehicle Driver table
# 	lic_nos = frappe.db.sql("""select A.vehicle_driver from `tabVehicle Driver` A where A.parent = '%s';""" % (vehicleno), as_dict=1)
# 	lst_lic_nos = []

# 	#Get a list of license nos from returned values.
# 	for ln in lic_nos:
# 		lst_lic_nos.append(ln.vehicle_driver)

# 	#Load drivers from license nos.
# 	dl = frappe.get_all("Driver", fields="*", filters={"wb_driver_licence" : ["in", lst_lic_nos]}, order_by="wb_driver_fn")
# 	return dl


	
def driver_query(doctype, txt, searchfield, start, page_len, filters):
	#lic_nos = frappe.db.sql("""select A.vehicle_driver from `tabVehicle Driver` A where A.parent = '%s';""" % (vehicleno), as_dict=1)

	return frappe.db.sql("""select A.* from `tabDriver` as A 
		INNER JOIN `tabVehicle Driver` as B ON A.name = B.vehicle_driver
        where B.parent = '{vehicleno}' 
            and ({key} like %(txt)s
                or wb_driver_fn like %(txt)s
                or wb_licence_no like %(txt)s)
            {mcond}
        order by
            if(locate(%(_txt)s, A.name), locate(%(_txt)s, A.name), 99999),
            if(locate(%(_txt)s, wb_driver_fn), locate(%(_txt)s, wb_driver_fn), 99999),
            if(locate(%(_txt)s, wb_licence_no), locate(%(_txt)s, wb_licence_no), 99999),
            A.name, wb_driver_fn
        limit %(start)s, %(page_len)s""".format(**{
            'key': searchfield,
            'vehicleno': filters.get('vehicleno'),
            'mcond':get_match_cond(doctype)
        }), {
            'txt': "%%%s%%" % txt,
            '_txt': txt.replace("%", ""),
            'start': start,
            'page_len': page_len
        })

def driver_query_2(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select A.wb_driver_licence, A.wb_driver_fn, A.wb_driver_ln from `tabDriver` as A 
		INNER JOIN `tabVehicle Driver` as B ON A.name = B.vehicle_driver
        where B.parent = '{vehicleno}' 
            """.format(vehicleno=filters.get("vehicleno")))