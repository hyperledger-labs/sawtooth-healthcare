var m = require("mithril")
//var Client = require("../models/Client")

module.exports = {
//    oninit: Client.loadList,
    view: function(vnode) {
        return m("main.layout", [
            m("nav.menu", [
//                m("a[href='/actions']", {oncreate: m.route.link}, "Actions|"),
//                m("a[href='/clinic_list']", {oncreate: m.route.link}, "Clinics|"),
//                m("a[href='/doctor_list']", {oncreate: m.route.link}, "Doctors|"),
//                m("a[href='/patient_list']", {oncreate: m.route.link}, "Patients|"),
//                m("a[href='/lab_test_list']", {oncreate: m.route.link}, "Lab Tests|"),
//                m("a[href='/lab_test_list/new/']", {oncreate: m.route.link}, "Add Lab Test|"),
//                m("a[href='/pulse_list']", {oncreate: m.route.link}, "Pulse List|"),
//                m("a[href='/pulse_list/new/']", {oncreate: m.route.link}, "Add Pulse|"),
                m("a", {href: "/clinic", oncreate: m.route.link}, "As Clinic|"),
                m("a", {href: "/doctor", oncreate: m.route.link}, "As Doctor|"),
                m("a", {href: "/patient", oncreate: m.route.link}, "As Patient|"),
                m("a", {href: "/lab", oncreate: m.route.link}, "As Lab"),
            ]),
            m("section", vnode.children),
        ])
    }
}