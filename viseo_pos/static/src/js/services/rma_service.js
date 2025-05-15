function getAllVehicleRmaMecano(odooClient,uid,traiteData){
    return odooClient._rpc({
        model: 'v.smart.vehicle.employee',
        method: 'search_read',
        args: [
            [
                ['hr_employee_id', '!=', false],
                ['user_id','=',uid],['is_task_no_end', '=', true],
                ['state_ro','=','repair']
            ],
            ['id', 'name2', 'vehicle_id', 'hr_employee_id','license_plate','vin_sn','brand_id','model_id','rma_id','vehicle_type',
              'number_task','task_end','is_task_no_end','customer_id'
            ]
        ],
       }).then(data => {
        // console.log("data retouner",data)
        traiteData(data)
    }).catch(error => {
        console.error("Erreur chargement", error);
    });
}

function getAllTaskVehicleRma(odooClient,rma_id,traiteData){
    //  console.log("rma_id",rma_id)
    return odooClient._rpc({
        model: 'v.service.product.list',
        method: 'search_read',
        args: [
            [['repair_id', '=', rma_id]],
            ['id', 'namelibre', 'operation_done', 'product_id','product_qty','repair_id','service_work_id'
                ,'service_product_list_id','hr_employee_id','user_id','date_start_service','date_end_service','state_follow','hr_employee_service_prod_list_id']
        ],
       }).then(data => {
         console.log("data task vehicle rma",data)
        traiteData(data)
    }).catch(error => {
        console.error("Erreur chargement", error);
    });
}

function apiStart(odooClient,service_id,traite){
//   console.log("start task",service_id)
  return odooClient._rpc({
    model: 'hr_employee.service.product.list.rel',
    method: 'commencer',
    args: [service_id]  
  }).then(data => {
    //   console.log("commencer", data);
      traite()
  }).catch(error => {
      console.error("Erreur chargement", error);
  });
}

    
function apiEnd(odooClient,service_id,traite){
//   console.log("end task",service_id)
  return odooClient._rpc({
    model: 'hr_employee.service.product.list.rel',
    method: 'terminer',
    args: [service_id]  
  }).then(data => {
    //   console.log("terminer", data);
      traite()
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
    document.getElementById("vin-details").textContent = vehicleRma.vin_sn
    document.getElementById("plaque-details").textContent = vehicleRma.license_plate
    document.getElementById("details-vehicle-head").innerHTML = html;
}
function insertTacheVehicleInHtml(qweb,listeTacheVehicle){
    const html = qweb.render('PageListTacheVehicleRma', { taskVehicleRma: listeTacheVehicle });
    // console.log(html)
    document.getElementById("details-vehicle-tache").innerHTML = html;
}

function insertListVehicleInHtml(qweb,dataVehicle){
  const html = qweb.render('PageListeVehicleRma', { dataVehicle: dataVehicle });
  // console.log(html)
  document.getElementById("main-vehicle").innerHTML = html;
}

function w3_open() {
    if (window.innerWidth <= 800) { // Mobile
        document.getElementById("main-vehicle").style.marginRight = "0%";
        document.getElementById("details-vehicle").style.width = "100%";
    } else { // Desktop
        document.getElementById("main-vehicle").style.marginRight = "50%";
        document.getElementById("details-vehicle").style.width = "50%";
        responsive_open()
    }
    document.getElementById("details-vehicle").style.display = "block";
}

function responsive_open(){
  const items = document.querySelectorAll('.vehicle-item');
  console.log("responsive",items)
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

function w3_close() {
    document.getElementById("main-vehicle").style.marginRight = "0%";
    document.getElementById("details-vehicle").style.display = "none";
    document.getElementById("details-vehicle-head").innerHTML = ""
    const items = document.querySelectorAll('.vehicle-item');
    items.forEach(el => {
        el.className = 'vehicle-item col-sm-6 col-lg-4 col-md-6 mb-3';
    });
}

function taskVehicleRmaSortByRepairId(data){
    return data.sort((a, b) => a.repair_id - b.repair_id);
}

function taskVehicleGroupByRma(data,uid){
    let group = Object.groupBy(data,({ service_product_list_id }) => service_product_list_id)
    // console.log("GROUP",group)
    let result = []
    for (const [key, value] of Object.entries(group)) {
        let obj = null;
        for (let i = 0; i < value.length; i++) {
            obj = value[i];
            obj['assigne'] = false;
            if(value[i].user_id && value[i].user_id[0] === uid){
                obj['assigne'] = true;
                break;
            }
        }
        result.push(obj);
    }
    // console.log("Traiter",result)
    return result;
}

function getTaskAssigne(data){
    return data.filter(item => item.assigne);
}

function getTaskEnd(data){
  return data.filter(item => item.date_end_service && item.date_start_service);
}

function getTaskNotStart(data){
  return data.filter(item => !item.date_start_service);
}

function showTaskAssigneAndNo(task,notask,end,noEnd){
    document.getElementById("taskNonAssigneid").textContent = notask;
    document.getElementById("taskAssigneid").textContent = task;
    document.getElementById("taskNotStartid").textContent = end;
    // document.getElementById("taskNotEndid").textContent = noEnd; 
}



