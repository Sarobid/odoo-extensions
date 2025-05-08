function getAllVehicleRmaMecano(odooClient,uid,traiteData){
    return odooClient._rpc({
        model: 'v.smart.vehicle.employee',
        method: 'search_read',
        args: [
            [['hr_employee_id', '!=', false],
                // ['user_id','=',uid]
            ],
            ['id', 'name2', 'vehicle_id', 'hr_employee_id','license_plate','vin_sn','brand_id','model_id','rma_id','vehicle_type']
        ],
       }).then(data => {
        console.log("data retouner",data)
        traiteData(data)
    }).catch(error => {
        console.error("Erreur chargement", error);
    });
}

function getAllTaskVehicleRma(odooClient,rma_id,traiteData){
    // console.log("rma_id",rma_id)
    return odooClient._rpc({
        model: 'v.service.product.list',
        method: 'search_read',
        args: [
            [['repair_id', '=', rma_id]],
            ['id', 'namelibre', 'operation_done', 'product_id','product_qty','repair_id','service_work_id']
        ],
       }).then(data => {
        console.log("data task vehicle rma",data)
        traiteData(data)
    }).catch(error => {
        console.error("Erreur chargement", error);
    });
}

function getDetailsRma(dataFilter,rmaid){
    return dataFilter.filter(item =>item.id === rmaid);
}

function insertDetailsVehicleInHtml(qweb,vehicleRma){
    const html = qweb.render('PageDetailsVehicleRma', { vehicle: vehicleRma });
    // console.log(html)
    document.getElementById("details-vehicle-head").innerHTML = html;
}
function insertTacheVehicleInHtml(qweb,listeTacheVehicle){
    const html = qweb.render('PageListTacheVehicleRma', { taskVehicleRma: listeTacheVehicle });
    // console.log(html)
    document.getElementById("details-vehicle-tache").innerHTML = html;
}

function w3_open() {
    const items = document.querySelectorAll('.vehicle-item');
    if (window.innerWidth <= 800) { // Mobile
        document.getElementById("main-vehicle").style.marginRight = "0%";
        document.getElementById("details-vehicle").style.width = "100%";
    } else { // Desktop
        document.getElementById("main-vehicle").style.marginRight = "50%";
        document.getElementById("details-vehicle").style.width = "50%";
        if(window.innerWidth <= 900){
            items.forEach(el => {
                el.className = 'vehicle-item col-12 mb-3';
            });
        }else{
            items.forEach(el => {
                el.className = 'vehicle-item col-6 mb-3';
            });
        }

    }
    document.getElementById("details-vehicle").style.display = "block";
}

function w3_close() {
    document.getElementById("main-vehicle").style.marginRight = "0%";
    document.getElementById("details-vehicle").style.display = "none";
    document.getElementById("details-vehicle-head").innerHTML = ""
    const items = document.querySelectorAll('.vehicle-item');
    items.forEach(el => {
        el.className = 'vehicle-item col-sm-6 col-lg-4 col-md-6 mb-3';
    });

}



