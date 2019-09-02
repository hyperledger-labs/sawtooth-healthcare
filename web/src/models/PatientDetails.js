var m = require("mithril")

var PatientDetails = {
    pulseList: [],
    error: "",
    load: function(patient_pkey, doctor_pkey) {
        return m.request({
            method: "GET",
            url: "/api/pulse/" + patient_pkey + "/" + doctor_pkey,
//            withCredentials: true,
        })
        .then(function(result) {
            PatientDetails.error = ""
            PatientDetails.pulseList = result.data
        })
        .catch(function(e) {
            console.log(e)
            PatientDetails.error = e.message
        })
    },

//    current: {},

}

module.exports = PatientDetails