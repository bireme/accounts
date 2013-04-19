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

                    <ul class="nav nav-tabs">
                        <li class="active"><a href="#">Data</a></li>
                        <li><a href="#">Included Centers</a></li>
                    </ul>

                    <div class="block-data">
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
                                </div>

                                <div class='field'>
                                    <label for="field">Acronym</label>
                                    <input type='text'>
                                </div>

                                <div class='field'>
                                    <label for="field">Coordinating Center</label>
                                    <select>
                                        <option>BR1.1</option>
                                        <option>BR1.4</option>
                                    </select>
                                </div>
                            </fieldset>

                            <div class="control-panel form-submit">
                                <button class="btn btn-primary btn-large">Submit</button>
                            </div>
                        </form>
                    </div>

                    <div class="block-data">
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
                                    <th><a href="#">#</a></th>
                                    <th><a href="#">Code <i class='icon-caret-down'></i></a></th>
                                    <th><a href="#">Coordinator <i class='icon-caret-up'></i></a></th>
                                    <th><a href="#">Actions</a></th>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><input type='checkbox'></td>
                                        <td><a href="#">1</a></td>
                                        <td>BR1.1</td>
                                        <td>Maria Imaculada</td>
                                        <td>
                                            <a href="#" class='btn btn-mini'><i class='icon-pencil'></i></a>
                                            <a href="#" class='btn btn-mini'><i class='icon-remove'></i></a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><input type='checkbox'></td>
                                        <td><a href="#">1</a></td>
                                        <td>BR1.1</td>
                                        <td>Maria Imaculada</td>
                                        <td>
                                            <a href="#" class='btn btn-mini'><i class='icon-pencil'></i></a>
                                            <a href="#" class='btn btn-mini'><i class='icon-remove'></i></a>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>

                            <? include 'pagination.php' ?>              
                        </div>  
                    </div>                    
                </div>                
            </div>
            <? include 'footer.php' ?>
        </div>
    </body>
</html>