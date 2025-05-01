$(document).ready(function(){

    const allSitesCount = parseInt($('#allSitesCount').text());
    const sitesTable = $('#sitesTable');
    const sitesTableError = $('#sitesTableError');
    const sites = '/projetos';
    const okSitesCount = $('#okSitesCount');
    const errorSitesCount = $('#errorSitesCount');
    const verify = $('#verify');
    const progressBar = $('progress');

    let sitesCount = 0;
    let sitesError = 0;
    let sitesOk = 0;
    let percent = 0;

    
    $("#buscar").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $(".table tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    $("#buscarPainel").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $(".table tr td input[type='text']").filter(function() {
            $(this).parent().parent().toggle($(this).val().toLowerCase().indexOf(value) > -1)
        });
    });

    function increaseLoading(status){
        sitesCount++;
        if(status == 200) {
            sitesOk++;
            okSitesCount.text(sitesOk);
        }else{
            sitesError++;
            errorSitesCount.text(sitesError);
        }
        percent = sitesCount*100/allSitesCount;
        progressBar.val(percent);
        if (percent == 100){
            verify.removeAttr('disabled');
        }
        
    }

    function getSites(sites){
        $.ajax({
            url: sites,
            method: 'GET',
            success: function(response) {
                response.map(function(site) {
                    getStatus(site);
                });
            }
        });
    }

    function getStatus(site){
        $.ajax({
            url: site,
            method: 'GET',
            dataType: 'jsonp',
            success: function(data, textStatus, xhr) {
                appendResult(site, xhr.status);
            },
            error: function(xhr, ajaxOptions, thrownError){
                console.log(xhr.status)
                appendResult(site, xhr.status);
            }
        });
    }

    function appendResult(url, status){
        if (status == 200){
            trColor = 'success';
            tbody = sitesTable;
        }else{
            trColor = 'danger';
            tbody = sitesTableError;
        }
        tbody.append(
            `<tr class="tr-background-${trColor}">
                <td><a href="${url}" target="_blank">${url}</a></td>
                <td class="">${status}</td>
            </tr>`
        );
        increaseLoading(status);
    }

    verify.click(function() {
        verify.attr('disabled', 'disabled');
        progressBar.val(0);
        getSites(sites);
    });

    // ======================= PAINEL ==========================
    
    const painelProtocol =  $('.painelProtocol');
    const painelEditar =  $('.painelEditar');
    const painelSalvar =  $('.painelSalvar');

    painelSalvar.hide();


    painelProtocol.each(function() {
        $(this).val($(this).data('selected'));
    });

    painelEditar.click(function() {
        $(this).hide();
        $(this).parent().find(painelSalvar).show();
        $(this).parent().parent().find('select, input').removeAttr('disabled');
    });

  
});