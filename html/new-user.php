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
            </ul>
            

            <div class="container-fluid content main">
                <!--  header -->
                <div class='header'>
                    <h2><i class='icon-user'></i> Register New User</h2>
                </div>

                <? include 'help.php' ?>

                <div class='body'>

                    <ul class="nav nav-tabs">
                        <li class="active"><a href="#">Data</a></li>
                        <li><a href="#">Permissions</a></li>
                    </ul>

                    <div class="block-data">
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
                                        <option>Superuser</option>
                                    </select>
                                </div>
                            </fieldset>

                            <div class="control-panel form-submit">
                                <button class="btn btn-primary btn-large">Submit</button>
                            </div>
                        </form>
                    </div>

                    <div class="block-permission">
                        
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
            <? include 'footer.php' ?>
        </div>
    </body>
</html>