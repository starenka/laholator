Laholátor : Simple app for text generation form given samples
========================================================

Laholátor allows you to generate random text based on ngram sample analysis done by NLTK (http://www.nltk.org/).
This particular app generates text based on work by JUDr.PhDr.Mgr. et Mgr.Henryk Lahola, but you can make it work
for any other texts by modifying the samples db. It's build on Flask (http://flask.pocoo.org/) web framework.

Setup
-----

To setup the app, just edit your settings either in settings/base.py, settings/production.py or settings/local_empty.py to suit your needs. If you edit local_empty.py be sure to copy it as local.py in order to get loaded. The wsgi file should work w/out any tuning. Consult your web server docs to make wsgi work with your server. Sample vhost file for Apache would look like this:

    root@kosmik1:/home/starenka# cat /etc/apache2/sites-available/laholator
        <VirtualHost 127.0.0.1:80>
            ServerName laholator
                WSGIDaemonProcess laholator user=starenka group=starenka threads=5
                WSGIScriptAlias / /www/laholator/laholator.wsgi

                <Directory /www/laholator>
                    WSGIProcessGroup laholator
                    WSGIApplicationGroup %{GLOBAL}
                    WSGIScriptReloading On
                    Order deny,allow
                    Allow from all
                </Directory>
        </VirtualHost>

Have fun!

