const rma_follow_service = {
    follow_upgrade : function (odooClient,hr_emp_service_prod_id,methodeName,traite){
        return odooClient._rpc({
          model: 'follow.hr.emp.service.prod',
          method: methodeName,
          args: [hr_emp_service_prod_id]  
        }).then(data => {
             console.log("follow_upgrade", data);
            traite()
        }).catch(error => {
            console.error("Erreur chargement", error);
        });
      },
    block_start : function (odooClient,hr_emp_service_prod_id,traite){
        return rma_follow_service.follow_upgrade(odooClient,hr_emp_service_prod_id,"start_block",traite)
    } ,
    block_end : function (odooClient,hr_emp_service_prod_id,traite){
        return rma_follow_service.follow_upgrade(odooClient,hr_emp_service_prod_id,"end_block",traite)
    } ,
    break_start : function (odooClient,hr_emp_service_prod_id,traite){
        return rma_follow_service.follow_upgrade(odooClient,hr_emp_service_prod_id,"start_break",traite)
    } ,
    break_end : function (odooClient,hr_emp_service_prod_id,traite){
        return rma_follow_service.follow_upgrade(odooClient,hr_emp_service_prod_id,"end_break",traite)
    }
}
