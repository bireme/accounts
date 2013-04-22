<!DOCTYPE html>
<html>
    <? include 'head.php' ?>
    <body>
        <div class='mask'><img src='static/image/loading.gif'></div>
        <div class="wrap">
            <? include 'menu.php' ?>

            
            <ul class="breadcrumb">
                <li><a href="#">Home</a> <span class="divider">/</span></li>
                <li><a href="#">Network</a><span class="divider">/</span></li>
                <li class="active">New</li>
            </ul>
            

            <div class="container-fluid content main">
                <!--  header -->
                <div class='header'>
                    <h2><i class='icon-sitemap'></i> Register New Network</h2>
                </div>

                <? include 'help.php' ?>

                <div class='body'>

                    <ul class="nav nav-tabs" id='tab'>
                        <li class="active"><a href="#tab-data" data-toggle="tab">Data</a></li>
                        <li><a href="#tab-centers" data-toggle="tab">Included Centers</a></li>
                    </ul>

                    <div class="tab-content">
                        <div id="tab-data" class="tab-pane active">
                            <form>
                                <fieldset>                                
                                    <div class='field'>
                                        <label for="field">Country</label>
                                        <select>
                                            <option>Brasil</option>
                                            <option>Argentina</option>
                                            <option>EUA</option>
                                        </select>
                                    </div>

                                    <div class='field'>
                                        <label for="field">Topic</label>
                                        <select>
                                            <option>BVS Chile</option>
                                            <option>PEPSIC</option>
                                        </select>

                                        <a href="#" class='btn'><i class='icon-plus'></i></a>
                                    </div>

                                    <div class='field'>
                                        <label for="field">Acronym</label>
                                        <input type='text'>
                                    </div>

                                    <div class='field'>
                                        <label for="field">Coordinating Center</label>
                                        <input type='text' id='id_coordinating_center'>
                                    </div>
                                </fieldset>

                                <div class="control-panel form-submit">
                                    <button class="btn btn-primary btn-large">Submit</button>
                                </div>
                            </form>
                        </div>
                        <div id='tab-centers' class="tab-pane">
                            <div class='body'>
                                <div class='pull-right'>
                                    <div class="input-append">
                                        <input type='text' name="s" placeholder="Type your center">
                                        <button class="btn" type="button"><i class='icon-search'></i></button>
                                    </div>
                                </div>

                                <table class='table'>
                                    <thead>
                                        <th></th>
                                        <th><a href="#">Code <i class='icon-caret-down'></i></a></th>
                                        <th><a href="#">Institution <i class='icon-caret-up'></i></a></th>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td><input type='checkbox'></td>
                                            <td>BR1.1</td>
                                            <td>Universidade de São Paulo</td>
                                        </tr>
                                    </tbody>
                                </table>

                                <? include 'pagination.php' ?>              
                            </div>  
                        </div>                    
                    </div>

                </div>                
            </div>
            <? include 'footer.php' ?>
        </div>

        <!-- tab js -->
        <script>
            $(function(){
                $("#tab a:first").tab('show');

                $('#id_coordinating_center').typeahead({
                    source: ['BR1.1', 'BR1.2', 'BR1.15', 'BR95.1', 'CL1.1']
                });
            });
        </script>
    </body>
</html>