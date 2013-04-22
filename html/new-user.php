<!DOCTYPE html>
<html>
    <? include 'head.php' ?>
    <body>
        <div class='mask'><img src='static/image/loading.gif'></div>
        <div class="wrap">
            <? include 'menu.php' ?>

            
            <ul class="breadcrumb">
                <li><a href="#">Home</a> <span class="divider">/</span></li>
                <li><a href="#">User</a><span class="divider">/</span></li>
                <li class="active">New</li>

                <li class='pull-right'><a href="javascript: show_help();" title="Show help"><i class='icon-question-sign'></i></a></li>
            </ul>
            

            <div class="container-fluid content main">
                <!--  header -->
                <div class='header'>
                    <h2><i class='icon-user'></i> Register New User</h2>
                </div>

                <? include 'help.php' ?>

                <div class='body'>

                    <ul class="nav nav-tabs" id="tab">
                        <li class="active"><a href="#tab-data" data-toggle="tab">Data</a></li>
                        <li><a href="#tab-permissions" data-toggle="tab">Permissions</a></li>
                    </ul>

                    <div class="tab-content">
                        <div id="tab-data" class='tab-pane active'>
                            <form>
                                <fieldset>                                
                                    <div class='field'>
                                        <label for="field">Name</label>
                                        <input type='text'>
                                    </div>
                                    
                                    <div class='field'>
                                        <label for="field">Email</label>
                                        <input type='text'>
                                    </div>

                                    <div class='field'>
                                        <label for="field">Type</label>
                                        <select>
                                            <option>Normal</option>
                                            <option>Advanced</option>
                                        </select>
                                    </div>

                                    <div class='field'>
                                        <label for="field">
                                            <input type="checkbox">
                                            Is Superuser?
                                        </label>
                                    </div>

                                    <div class='field'>
                                        <label for="field">
                                            <input type="checkbox">
                                            Is Active?
                                        </label>
                                    </div>
                                </fieldset>

                                <div class="control-panel form-submit">
                                    <button class="btn btn-primary btn-large">Submit</button>
                                </div>
                            </form>
                        </div>
                        <div id="tab-permissions" class='tab-pane'>
                            
                            <ul>
                                <li>
                                    <h3>Diretório de Eventos <small>DIREVE</small></h3>
                                    <div class="checkboxes">
                                        <input type="checkbox"> Documentalist
                                        <input type="checkbox"> Editor
                                        <input type="checkbox"> Administrator
                                    </div>
                                </li>

                                <li>
                                    <h3>Lilacs Descrição Bibliográfica e Indexação <small>LILDBI-Web</small></h3>
                                    <div class="checkboxes">
                                        <input type="checkbox"> Documentalist
                                        <input type="checkbox"> Editor
                                        <input type="checkbox"> Administrator
                                    </div>
                                </li>
                            </ul>
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
            });
        </script>
    </body>
</html>