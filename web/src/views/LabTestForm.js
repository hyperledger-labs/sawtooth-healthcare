var m = require("mithril")
var LabTest = require("../models/LabTest")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function(vnode) {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    LabTest.add(vnode.attrs.client_key)
                }
            }, [
            m("label.label", "HEIGHT (CM)"),
            m("input.input[type=text][placeholder=HEIGHT (CM)]", {
                oninput: m.withAttr("value", function(value) {LabTest.current.height = value}),
                value: LabTest.current.height
            }),
            m("label.label", "WEIGHT (KG)"),
            m("input.input[placeholder=WEIGHT (KG)]", {
                oninput: m.withAttr("value", function(value) {LabTest.current.weight = value}),
                value: LabTest.current.weight
            }),
            m("label.label", "GENDER (MALE OR FEMALE)"),
            m("input.input[placeholder=GENDER (MALE OR FEMALE)]", {
                oninput: m.withAttr("value", function(value) {LabTest.current.gender = value}),
                value: LabTest.current.gender
            }),
            m("label.label", "A/G RATIO"),
            m("input.input[placeholder=A/G RATIO]", {
                oninput: m.withAttr("value", function(value) {LabTest.current.a_g_ratio = value}),
                value: LabTest.current.a_g_ratio
            }),
            m("label.label", "ALBUMIN"),
            m("input.input[placeholder=ALBUMIN]", {
                oninput: m.withAttr("value", function(value) {LabTest.current.albumin = value}),
                value: LabTest.current.albumin
            }),
            m("label.label", "ALKALINE PHOSPHATASE"),
            m("input.input[placeholder=ALKALINE PHOSPHATASE]", {
                oninput: m.withAttr("value", function(value) {LabTest.current.alkaline_phosphatase = value}),
                value: LabTest.current.alkaline_phosphatase
            }),
            m("label.label", "APPEARANCE"),
            m("input.input[placeholder=APPEARANCE]", {
                oninput: m.withAttr("value", function(value) {LabTest.current.appearance = value}),
                value: LabTest.current.appearance
            }),
            m("label.label", "BILIRUBIN"),
            m("input.input[placeholder=BILIRUBIN]", {
                oninput: m.withAttr("value", function(value) {LabTest.current.bilirubin = value}),
                value: LabTest.current.bilirubin
            }),
            m("label.label", "CASTS"),
            m("input.input[placeholder=CASTS]", {
                oninput: m.withAttr("value", function(value) {LabTest.current.casts = value}),
                value: LabTest.current.casts
            }),
            m("label.label", "COLOR"),
            m("input.input[placeholder=COLOR]", {
                oninput: m.withAttr("value", function(value) {LabTest.current.color = value}),
                value: LabTest.current.color
            }),
            m("button.button[type=submit]", "Add"),
            m("label.error", LabTest.error)
        ])
    }
}