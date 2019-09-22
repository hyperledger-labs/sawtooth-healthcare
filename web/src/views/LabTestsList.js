var m = require("mithril")
var LabTest = require("../models/LabTest")

module.exports = {
    oninit:
        function(vnode){
            LabTest.loadList(vnode.attrs.client_key)
        },
//    oninit: LabTest.loadList,
    view: function() {
        return m(".user-list", LabTest.list.map(function(lt) {
            return m("a.user-list-item", "NAME: " + lt.name + "; " +
                                    "SURNAME: " + lt.surname + "; " +
                                    "HEIGHT (CM): " + lt.height + "; " +
                                    "WEIGHT (KG): " + lt.weight + "; " +
                                    "GENDER (MALE OR FEMALE): " + lt.gender + "; " +
                                    "A/G RATIO: " + lt.a_g_ratio + "; " +
                                    "ALBUMIN: " + lt.albumin + "; " +
                                    "ALKALINE PHOSPHATASE: " + lt.alkaline_phosphatase + "; " +
                                    "APPEARANCE: " + lt.appearance + "; " +
                                    "BILIRUBIN: " + lt.bilirubin + "; " +
                                    "CASTS: " + lt.casts + "; " +
                                    "COLOR: " + lt.color + ";"
                                    ) // + user.publicKey
        }),
        m("label.error", LabTest.error))
    }
}