var m = require("mithril")

module.exports = {
    view: function(vnode) {
        return m("main.layout", [
            m("nav.menu", [
                m("a[href='/actions']", {oncreate: m.route.link}, "Actions"),
                m("a[href='/clinic_list']", {oncreate: m.route.link}, "Clinics"),
                m("a[href='/doctor_list']", {oncreate: m.route.link}, "Doctors"),
                m("a[href='/patient_list']", {oncreate: m.route.link}, "Patients"),
                m("a[href='/lab_test_list']", {oncreate: m.route.link}, "Lab Tests"),
                m("a[href='/lab_test_list/new/']", {oncreate: m.route.link}, "Add Lab Test"),
                m("a[href='/pulse_list']", {oncreate: m.route.link}, "Pulse List"),
                m("a[href='/pulse_list/new/']", {oncreate: m.route.link}, "Add Pulse"),
            ]),
            m("section", vnode.children),
        ])
    }
}