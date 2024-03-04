frappe.ui.form.on("Item",{
    refresh:function(frm){
        console.log("innnnnnnnnn")
        frm.add_custom_button(__("Send Email"), function(){
            frappe.call({
                method: "citrus_app.custom.item.send_email",
                args:{
                    item_code:frm.doc.name
                },
                callback: function(r){
                    console.log(r)
                }
            })
        },__("Actions"));
    }
})