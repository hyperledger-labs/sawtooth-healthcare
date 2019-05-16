var m = require("mithril")

//var UserList = require("./views/UserList")
//var UserForm = require("./views/UserForm")

//var DoctorForm = require("./views/DoctorForm")
var DoctorList = require("./views/DoctorList")
var PatientList = require("./views/PatientList")
var ClinicList = require("./views/ClinicList")
var ClaimList = require("./views/ClaimList")
var ClaimDetailsForm = require("./views/ClaimDetailsForm")
var PatientForm = require("./views/PatientForm")
var DoctorAssignForm = require("./views/DoctorAssignForm")
var ClaimNewForm = require("./views/ClaimNewForm")
var ActionsList = require("./views/ActionsList")
var Layout = require("./views/Layout")

m.route(document.body, "/actions", {

    "/actions": {
        render: function() {
            return m(Layout, m(ActionsList))
//              return m(ActionsList)
        }
    },
    "/patient_list": {
        render: function() {
            return m(Layout, m(PatientList))
        }
    },
    "/patient/new/": {
        render: function() {
            return m(Layout, m(PatientForm))
        }
    },
    "/doctor_list": {
        render: function() {
            return m(Layout, m(DoctorList))
        }
    },
    "/clinic_list": {
        render: function() {
            return m(Layout, m(ClinicList))
        }
    },
    "/claim_list": {
        render: function() {
            return m(Layout, m(ClaimList))
        }
    },
    "/doctor/assign/": {
        render: function() {
            return m(Layout, m(DoctorAssignForm))
        }
    },
    "/claim/new/": {
        render: function() {
            return m(Layout, m(ClaimNewForm))
        }
    },
    "/claim/:clinic_pkey/:claim_id": {
        render: function(vnode) {
            return m(Layout, m(ClaimDetailsForm, vnode.attrs))
        }
    },
//    "/list": {
//        render: function() {
//            return m(Layout, m(UserList))
//        }
//    },
//    "/edit/:id": {
//        render: function(vnode) {
//            return m(Layout, m(UserForm, vnode.attrs))
//        }
//    },
})