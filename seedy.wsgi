# coding=utf-8
#
# $Id: $
#
# NAME:         seedy.wsgi
#
# AUTHOR:       Nick Whalen <nickw@mindstorm-networks.net>
# COPYRIGHT:    2013 by Nick Whalen
# LICENSE:
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# DESCRIPTION:
#   WSGI entry point for webapp
#


from seedyweb import seedy_web_service as application

if __name__ == '__main__':
    # Runs a basic web server
    application.debug = True
    application.run(host='0.0.0.0', port=8080)
else:
    application.run()