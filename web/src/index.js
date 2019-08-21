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

var LabTestsList = require("./views/LabTestsList")
var LabTestForm = require("./views/LabTestForm")

var PulseList = require("./views/PulseList")
var PulseForm = require("./views/PulseForm")

var DoctorAssignForm = require("./views/DoctorAssignForm")
var FirstVisitForm = require("./views/FirstVisitForm")
var EatPillsForm = require("./views/EatPillsForm")
var PassTestsForm = require("./views/PassTestsForm")
var AttendProceduresForm = require("./views/AttendProceduresForm")
var NextVisitForm = require("./views/NextVisitForm")

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
    "/first_visit/": {
        render: function() {
            return m(Layout, m(FirstVisitForm))
        }
    },
    "/eat_pills/": {
        render: function() {
            return m(Layout, m(EatPillsForm))
        }
    },
    "/pass_tests/": {
        render: function() {
            return m(Layout, m(PassTestsForm))
        }
    },
    "/attend_procedures/": {
        render: function() {
            return m(Layout, m(AttendProceduresForm))
        }
    },
    "/next_visit/": {
        render: function() {
            return m(Layout, m(NextVisitForm))
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
    "/lab_test_list": {
        render: function() {
            return m(Layout, m(LabTestsList))
        }
    },
    "/lab_test_list/new/": {
        render: function() {
            return m(Layout, m(LabTestForm))
        }
    },
    "/pulse_list": {
        render: function() {
            return m(Layout, m(PulseList))
        }
    },
    "/pulse_list/new/": {
        render: function() {
            return m(Layout, m(PulseForm))
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