var m = require("mithril")

//var UserList = require("./views/UserList")
//var UserForm = require("./views/UserForm")

//var DoctorForm = require("./views/DoctorForm")
var DoctorList = require("./views/DoctorList")
var DoctorForm = require("./views/DoctorForm")

var PatientList = require("./views/PatientList")
var PatientForm = require("./views/PatientForm")

var ClinicList = require("./views/ClinicList")
var ClinicForm = require("./views/ClinicForm")

var ClaimList = require("./views/ClaimList")
var ClaimNewForm = require("./views/ClaimNewForm")
var ClaimDetailsForm = require("./views/ClaimDetailsForm")

var DoctorAssignForm = require("./views/DoctorAssignForm")
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
    "/doctor/new/": {
        render: function() {
            return m(Layout, m(DoctorForm))
        }
    },
    "/clinic_list": {
        render: function() {
            return m(Layout, m(ClinicList))
        }
    },
    "/clinic/new/": {
        render: function() {
            return m(Layout, m(ClinicForm))
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