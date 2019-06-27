var m = require("mithril")
//var User = require("../models/User")

module.exports = {
//    oninit: User.loadList,
//    view: function() {
//        return m(".user-list", User.list.map(function(user) {
//            return m("a.user-list-item", {href: "/edit/" + user.id, oncreate: m.route.link}, user.firstName + " " + user.lastName)
//        }))
//    }
    view: function() {
        return m(".user-list", [
//            m("a.user-list-item", {href: "/doctor/", oncreate: m.route.link}, "Create Doctor"),
            m("a.user-list-item", {href: "/doctor_list/", oncreate: m.route.link}, "Doctors List"),
            m("a.user-list-item", {href: "/doctor/new/", oncreate: m.route.link}, "New Doctor"),
            m("a.user-list-item", {href: "/clinic_list/", oncreate: m.route.link}, "Clinics List"),
            m("a.user-list-item", {href: "/clinic/new/", oncreate: m.route.link}, "New Clinic"),
            m("a.user-list-item", {href: "/patient_list/", oncreate: m.route.link}, "Patients List"),
            m("a.user-list-item", {href: "/patient/new/", oncreate: m.route.link}, "New Patient"),
            m("a.user-list-item", {href: "/claim_list/", oncreate: m.route.link}, "Claims List"),
            m("a.user-list-item", {href: "/claim/new/", oncreate: m.route.link}, "Register Claim"),
            m("a.user-list-item", {href: "/doctor/assign/", oncreate: m.route.link}, "Assign Doctor"),
            m("a.user-list-item", {href: "/first_visit/"}, "First Visit"),
            m("a.user-list-item", {href: "/eat_pills/"}, "Eat Pills"),
            m("a.user-list-item", {href: "/passtests/"}, "Pass Tests"),
            m("a.user-list-item", {href: "/attend_procedures/"}, "Attend Procedures"),
            m("a.user-list-item", {href: "/next_visit/"}, "Next Visit"),
        ])

    }
}