#!/usr/bin/env python3
"""
Git HTTP Server using git-http-backend
Exposes git repositories via HTTP for access through ngrok
"""

import os
import sys
import subprocess
import http.server
import cgi
import html
import base64
from urllib.parse import urlparse, unquote, parse_qs

# Configuration
GIT_REPO_DIR = "/home/sylaw/git/repositories"
GIT_HTTP_BACKEND = "/usr/lib/git-core/git-http-backend"
SERVER_PORT = 8080

class GitHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request()
    
    def do_POST(self):
        self.handle_request()
    
    def get_repo_branches(self, repo_path):
        """Get list of branches in repository"""
        try:
            result = subprocess.run(
                ['git', '--git-dir', repo_path, 'branch', '-a'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                branches = []
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('*'):
                        branch = line.replace('remotes/origin/', '').replace('remotes/', '')
                        if branch not in branches:
                            branches.append(branch)
                return branches if branches else ['main', 'master']
            return ['main', 'master']
        except:
            return ['main', 'master']
    
    def get_default_branch(self, repo_path):
        """Get default branch name"""
        try:
            result = subprocess.run(
                ['git', '--git-dir', repo_path, 'symbolic-ref', 'refs/remotes/origin/HEAD'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                branch = result.stdout.strip().replace('refs/remotes/origin/', '')
                return branch if branch else 'main'
            
            # Try to get main or master
            for branch in ['main', 'master']:
                result = subprocess.run(
                    ['git', '--git-dir', repo_path, 'show-ref', f'refs/heads/{branch}'],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return branch
            return 'main'
        except:
            return 'main'
    
    def get_file_tree(self, repo_path, branch, path=''):
        """Get file tree for a given path in repository"""
        try:
            # Use ls-tree with format to get type and name
            if path:
                git_path = f'{branch}:{path}'
            else:
                git_path = branch
            
            result = subprocess.run(
                ['git', '--git-dir', repo_path, 'ls-tree', git_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return []
            
            items = []
            for line in result.stdout.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                # Format: mode type object name
                # Example: 100644 blob abc123... file.txt
                #          040000 tree def456... directory/
                parts = line.split(None, 3)
                if len(parts) < 4:
                    continue
                
                mode, obj_type, obj_hash, item_name = parts
                full_path = os.path.join(path, item_name) if path else item_name
                
                if obj_type == 'tree' or mode.startswith('04'):
                    # It's a directory
                    items.append({
                        'name': item_name + '/',
                        'path': full_path,
                        'type': 'directory'
                    })
                else:
                    # It's a file (blob)
                    items.append({
                        'name': item_name,
                        'path': full_path,
                        'type': 'file'
                    })
            
            return sorted(items, key=lambda x: (x['type'] == 'file', x['name'].lower()))
        except Exception as e:
            return []
    
    def get_file_content(self, repo_path, branch, file_path):
        """Get content of a file from repository"""
        try:
            git_path = f'{branch}:{file_path}'
            result = subprocess.run(
                ['git', '--git-dir', repo_path, 'show', git_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return result.stdout
            return None
        except:
            return None
    
    def get_file_info(self, repo_path, branch, file_path):
        """Get file information (size, last commit, etc.)"""
        try:
            git_path = f'{branch}:{file_path}'
            result = subprocess.run(
                ['git', '--git-dir', repo_path, 'log', '-1', '--format=%H|%an|%ae|%ad|%s', '--date=iso', '--', git_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split('|')
                if len(parts) >= 5:
                    return {
                        'hash': parts[0],
                        'author': parts[1],
                        'email': parts[2],
                        'date': parts[3],
                        'message': parts[4]
                    }
            return None
        except:
            return None
    
    def render_repo_browser(self, repo_name, repo_path, branch=None, path=''):
        """Render repository file browser"""
        if branch is None:
            branch = self.get_default_branch(repo_path)
        
        branches = self.get_repo_branches(repo_path)
        
        # Get file tree
        items = self.get_file_tree(repo_path, branch, path)
        
        # Build breadcrumb
        breadcrumb = [{'name': repo_name, 'url': f'/{repo_name}/tree/{branch}'}]
        if path:
            parts = path.split('/')
            current_path = ''
            for part in parts:
                current_path = os.path.join(current_path, part) if current_path else part
                breadcrumb.append({
                    'name': part,
                    'url': f'/{repo_name}/tree/{branch}/{current_path}'
                })
        
        path_suffix = '/' + html.escape(path) if path else ''
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{html.escape(repo_name)} - File Browser</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f6f8fa;
            color: #24292e;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            padding: 20px;
        }}
        h1 {{
            margin: 0 0 20px 0;
            font-size: 24px;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 10px;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .breadcrumb {{
            margin-bottom: 15px;
        }}
        .breadcrumb a {{
            color: #0366d6;
            text-decoration: none;
        }}
        .breadcrumb a:hover {{
            text-decoration: underline;
        }}
        .breadcrumb span {{
            margin: 0 5px;
            color: #586069;
        }}
        .branch-selector {{
            margin-bottom: 15px;
        }}
        .branch-selector select {{
            padding: 5px 10px;
            border: 1px solid #d1d5da;
            border-radius: 3px;
            font-size: 14px;
        }}
        .file-list {{
            border: 1px solid #e1e4e8;
            border-radius: 3px;
        }}
        .file-item {{
            display: flex;
            align-items: center;
            padding: 8px 16px;
            border-bottom: 1px solid #eaecef;
        }}
        .file-item:last-child {{
            border-bottom: none;
        }}
        .file-item:hover {{
            background: #f6f8fa;
        }}
        .file-icon {{
            margin-right: 8px;
            width: 16px;
            text-align: center;
        }}
        .file-name {{
            flex: 1;
        }}
        .file-name a {{
            color: #0366d6;
            text-decoration: none;
        }}
        .file-name a:hover {{
            text-decoration: underline;
        }}
        .file-actions {{
            margin-left: 10px;
        }}
        .file-actions a {{
            color: #586069;
            text-decoration: none;
            margin-left: 10px;
        }}
        .file-actions a:hover {{
            color: #0366d6;
        }}
        .file-content {{
            background: #f6f8fa;
            border: 1px solid #e1e4e8;
            border-radius: 3px;
            padding: 16px;
            overflow-x: auto;
        }}
        .file-content pre {{
            margin: 0;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 12px;
            line-height: 1.45;
        }}
        .file-info {{
            background: #f6f8fa;
            border: 1px solid #e1e4e8;
            border-radius: 3px;
            padding: 10px;
            margin-bottom: 15px;
            font-size: 12px;
            color: #586069;
        }}
        .actions {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #eaecef;
        }}
        .actions a {{
            color: #0366d6;
            text-decoration: none;
            margin-right: 15px;
        }}
        .actions a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{html.escape(repo_name)}</h1>
        
        <div class="header">
            <div class="branch-selector">
                <label>Branch: </label>
                <select onchange="window.location.href='/{html.escape(repo_name)}/tree/' + this.value + '{path_suffix}'">
"""
        for b in branches:
            selected = 'selected' if b == branch else ''
            html_content += f'                    <option value="{html.escape(b)}" {selected}>{html.escape(b)}</option>\n'
        
        html_content += f"""
                </select>
            </div>
        </div>
        
        <div class="breadcrumb">
"""
        for i, crumb in enumerate(breadcrumb):
            if i > 0:
                html_content += '            <span>/</span>\n'
            html_content += f'            <a href="{crumb["url"]}">{html.escape(crumb["name"])}</a>\n'
        
        html_content += """
        </div>
"""
        
        if items:
            html_content += """
        <div class="file-list">
"""
            for item in items:
                icon = '📁' if item['type'] == 'directory' else '📄'
                if item['type'] == 'directory':
                    url = f'/{repo_name}/tree/{branch}/{item["path"]}'
                    html_content += f"""
            <div class="file-item">
                <span class="file-icon">{icon}</span>
                <span class="file-name"><a href="{url}">{html.escape(item["name"])}</a></span>
            </div>
"""
                else:
                    view_url = f'/{repo_name}/blob/{branch}/{item["path"]}'
                    html_content += f"""
            <div class="file-item">
                <span class="file-icon">{icon}</span>
                <span class="file-name"><a href="{view_url}">{html.escape(item["name"])}</a></span>
            </div>
"""
            html_content += """
        </div>
"""
        else:
            html_content += """
        <p>No files found in this directory.</p>
"""
        
        html_content += f"""
        <div class="actions">
            <a href="/{repo_name}.git">Clone Repository</a>
            <a href="/">Back to Repository List</a>
        </div>
    </div>
</body>
</html>
"""
        return html_content
    
    def render_file_view(self, repo_name, repo_path, branch, file_path):
        """Render file content view"""
        content = self.get_file_content(repo_path, branch, file_path)
        file_info = self.get_file_info(repo_path, branch, file_path)
        
        # Determine if file is binary or text
        is_binary = False
        if content:
            try:
                content.encode('utf-8')
            except:
                is_binary = True
        
        # Build breadcrumb
        breadcrumb = [{'name': repo_name, 'url': f'/{repo_name}/tree/{branch}'}]
        path_parts = file_path.split('/')
        current_path = ''
        for i, part in enumerate(path_parts[:-1]):
            current_path = os.path.join(current_path, part) if current_path else part
            breadcrumb.append({
                'name': part,
                'url': f'/{repo_name}/tree/{branch}/{current_path}'
            })
        breadcrumb.append({'name': path_parts[-1], 'url': ''})
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{html.escape(path_parts[-1])} - {html.escape(repo_name)}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f6f8fa;
            color: #24292e;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            padding: 20px;
        }}
        h1 {{
            margin: 0 0 20px 0;
            font-size: 24px;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 10px;
        }}
        .breadcrumb {{
            margin-bottom: 15px;
        }}
        .breadcrumb a {{
            color: #0366d6;
            text-decoration: none;
        }}
        .breadcrumb a:hover {{
            text-decoration: underline;
        }}
        .breadcrumb span {{
            margin: 0 5px;
            color: #586069;
        }}
        .file-info {{
            background: #f6f8fa;
            border: 1px solid #e1e4e8;
            border-radius: 3px;
            padding: 10px;
            margin-bottom: 15px;
            font-size: 12px;
            color: #586069;
        }}
        .file-content {{
            background: #ffffff;
            border: 1px solid #e1e4e8;
            border-radius: 3px;
            overflow: hidden;
        }}
        .file-content pre {{
            margin: 0;
            padding: 16px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 12px;
            line-height: 1.45;
            overflow-x: auto;
            background: #ffffff;
        }}
        .file-content code {{
            white-space: pre;
        }}
        .actions {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #eaecef;
        }}
        .actions a {{
            color: #0366d6;
            text-decoration: none;
            margin-right: 15px;
        }}
        .actions a:hover {{
            text-decoration: underline;
        }}
        .binary-warning {{
            padding: 20px;
            text-align: center;
            color: #586069;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{html.escape(path_parts[-1])}</h1>
        
        <div class="breadcrumb">
"""
        for i, crumb in enumerate(breadcrumb):
            if i > 0:
                html_content += '            <span>/</span>\n'
            if crumb['url']:
                html_content += f'            <a href="{crumb["url"]}">{html.escape(crumb["name"])}</a>\n'
            else:
                html_content += f'            <span>{html.escape(crumb["name"])}</span>\n'
        
        html_content += """
        </div>
"""
        
        if file_info:
            html_content += f"""
        <div class="file-info">
            <strong>Last modified:</strong> {html.escape(file_info.get('date', 'Unknown'))} by {html.escape(file_info.get('author', 'Unknown'))}<br>
            <strong>Commit:</strong> {html.escape(file_info.get('hash', '')[:8])} - {html.escape(file_info.get('message', ''))}
        </div>
"""
        
        if is_binary or not content:
            html_content += """
        <div class="binary-warning">
            <p>Binary file or file not found. Cannot display content.</p>
        </div>
"""
        else:
            escaped_content = html.escape(content)
            html_content += f"""
        <div class="file-content">
            <pre><code>{escaped_content}</code></pre>
        </div>
"""
        
        dir_path = '/'.join(path_parts[:-1])
        tree_url = f'/{repo_name}/tree/{branch}'
        if dir_path:
            tree_url += f'/{dir_path}'
        
        html_content += f"""
        <div class="actions">
            <a href="{tree_url}">View Directory</a>
            <a href="/{repo_name}/tree/{branch}">Repository Root</a>
            <a href="/{repo_name}.git">Clone Repository</a>
            <a href="/">Back to Repository List</a>
        </div>
    </div>
</body>
</html>
"""
        return html_content
    
    def handle_request(self):
        """Handle git HTTP requests"""
        parsed_path = urlparse(self.path)
        path = unquote(parsed_path.path)
        
        # Check if this is a git request
        is_git_request = (
            path.endswith('.git') or 
            '/info/refs' in path or 
            '/git-upload-pack' in path or 
            '/git-receive-pack' in path
        )
        
        if is_git_request:
            # Extract repository name and full path
            repo_name = None
            if '/info/refs' in path:
                repo_name = path.split('/info/refs')[0].lstrip('/')
            elif '/git-upload-pack' in path:
                repo_name = path.split('/git-upload-pack')[0].lstrip('/')
            elif '/git-receive-pack' in path:
                repo_name = path.split('/git-receive-pack')[0].lstrip('/')
            elif path.endswith('.git'):
                repo_name = path.lstrip('/')
            
            if repo_name:
                repo_path = os.path.join(GIT_REPO_DIR, repo_name)
                if os.path.exists(repo_path) and os.path.isdir(repo_path):
                    # Set environment variables for git-http-backend
                    env = os.environ.copy()
                    env['GIT_PROJECT_ROOT'] = GIT_REPO_DIR
                    env['GIT_HTTP_EXPORT_ALL'] = '1'
                    env['REQUEST_METHOD'] = self.command
                    env['PATH_INFO'] = '/' + path.lstrip('/')
                    env['QUERY_STRING'] = parsed_path.query
                    env['CONTENT_TYPE'] = self.headers.get('Content-Type', '')
                    env['CONTENT_LENGTH'] = self.headers.get('Content-Length', '0')
                    env['HTTP_USER_AGENT'] = self.headers.get('User-Agent', '')
                    
                    # Prepare git-http-backend command
                    cmd = [GIT_HTTP_BACKEND]
                    
                    # Execute git-http-backend
                    try:
                        process = subprocess.Popen(
                            cmd,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            env=env,
                            cwd=GIT_REPO_DIR
                        )
                        
                        # Send request body if present
                        if self.command == 'POST':
                            content_length = int(self.headers.get('Content-Length', 0))
                            if content_length > 0:
                                body = self.rfile.read(content_length)
                                stdout, stderr = process.communicate(input=body)
                            else:
                                stdout, stderr = process.communicate()
                        else:
                            stdout, stderr = process.communicate()
                        
                        # Check for errors
                        if process.returncode != 0:
                            error_msg = stderr.decode('utf-8', errors='ignore')
                            self.send_error(500, f"git-http-backend error: {error_msg}")
                            return
                        
                        # Parse response (git-http-backend outputs headers followed by body)
                        response_data = stdout
                        header_end = response_data.find(b'\r\n\r\n')
                        if header_end == -1:
                            header_end = response_data.find(b'\n\n')
                        
                        if header_end != -1:
                            header_data = response_data[:header_end]
                            body_data = response_data[header_end + 2:]
                            
                            # Parse headers
                            status_code = 200
                            headers = {}
                            for line in header_data.decode('utf-8', errors='ignore').split('\n'):
                                line = line.strip()
                                if not line:
                                    continue
                                if ':' in line:
                                    key, value = line.split(':', 1)
                                    key = key.strip().lower()
                                    value = value.strip()
                                    if key == 'status':
                                        try:
                                            status_code = int(value.split()[0])
                                        except:
                                            pass
                                    else:
                                        headers[key] = value
                            
                            # Send response
                            self.send_response(status_code)
                            for key, value in headers.items():
                                self.send_header(key, value)
                            self.end_headers()
                            
                            # Send body (may be binary)
                            self.wfile.write(body_data)
                        else:
                            # No headers, send raw response
                            self.send_response(200)
                            self.end_headers()
                            self.wfile.write(response_data)
                        
                    except Exception as e:
                        self.send_error(500, f"Error executing git-http-backend: {str(e)}")
                else:
                    self.send_error(404, "Repository not found")
            else:
                self.send_error(400, "Invalid git request")
        else:
            # Handle file browser requests
            path_parts = [p for p in path.split('/') if p]
            
            # Check for tree/blob routes: /repo-name/tree/branch/path or /repo-name/blob/branch/path
            if len(path_parts) >= 3 and path_parts[1] in ['tree', 'blob']:
                repo_name = path_parts[0]
                view_type = path_parts[1]  # 'tree' or 'blob'
                branch = path_parts[2]
                file_path = '/'.join(path_parts[3:]) if len(path_parts) > 3 else ''
                
                repo_full_name = repo_name + '.git'
                repo_path = os.path.join(GIT_REPO_DIR, repo_full_name)
                
                if os.path.exists(repo_path) and os.path.isdir(repo_path):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    
                    if view_type == 'blob':
                        html_content = self.render_file_view(repo_name, repo_path, branch, file_path)
                    else:  # tree
                        html_content = self.render_repo_browser(repo_name, repo_path, branch, file_path)
                    
                    self.wfile.write(html_content.encode('utf-8'))
                else:
                    self.send_error(404, "Repository not found")
            
            # Check for repository root: /repo-name (redirect to tree view)
            elif len(path_parts) == 1:
                repo_name = path_parts[0]
                repo_full_name = repo_name + '.git'
                repo_path = os.path.join(GIT_REPO_DIR, repo_full_name)
                
                if os.path.exists(repo_path) and os.path.isdir(repo_path):
                    # Redirect to tree view
                    default_branch = self.get_default_branch(repo_path)
                    self.send_response(302)
                    self.send_header('Location', f'/{repo_name}/tree/{default_branch}')
                    self.end_headers()
                else:
                    # Serve repository list
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    
                    html = """<!DOCTYPE html>
<html>
<head>
    <title>Git Repositories</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 40px 20px;
            background: #f6f8fa;
            color: #24292e;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            padding: 30px;
        }
        h1 {
            margin: 0 0 30px 0;
            font-size: 32px;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 15px;
        }
        ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        li {
            padding: 12px 0;
            border-bottom: 1px solid #eaecef;
        }
        li:last-child {
            border-bottom: none;
        }
        a {
            color: #0366d6;
            text-decoration: none;
            font-size: 16px;
        }
        a:hover {
            text-decoration: underline;
        }
        .repo-actions {
            margin-left: 15px;
            font-size: 12px;
            color: #586069;
        }
        .repo-actions a {
            font-size: 12px;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Available Git Repositories</h1>
        <ul>
"""
                    if os.path.exists(GIT_REPO_DIR):
                        repos = [d for d in os.listdir(GIT_REPO_DIR) 
                                if os.path.isdir(os.path.join(GIT_REPO_DIR, d)) and d.endswith('.git')]
                        for repo in sorted(repos):
                            repo_name = repo.replace('.git', '')
                            html += f'<li><a href="/{repo_name}">{repo_name}</a>'
                            html += f'<span class="repo-actions">'
                            html += f'<a href="/{repo_name}.git">[Clone]</a>'
                            html += f'</span></li>\n'
                    
                    html += """        </ul>
    </div>
</body>
</html>"""
                    self.wfile.write(html.encode('utf-8'))
            
            # Root path - serve repository list
            elif len(path_parts) == 0:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                
                html = """<!DOCTYPE html>
<html>
<head>
    <title>Git Repositories</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 40px 20px;
            background: #f6f8fa;
            color: #24292e;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            padding: 30px;
        }
        h1 {
            margin: 0 0 30px 0;
            font-size: 32px;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 15px;
        }
        ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        li {
            padding: 12px 0;
            border-bottom: 1px solid #eaecef;
        }
        li:last-child {
            border-bottom: none;
        }
        a {
            color: #0366d6;
            text-decoration: none;
            font-size: 16px;
        }
        a:hover {
            text-decoration: underline;
        }
        .repo-actions {
            margin-left: 15px;
            font-size: 12px;
            color: #586069;
        }
        .repo-actions a {
            font-size: 12px;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Available Git Repositories</h1>
        <ul>
"""
                if os.path.exists(GIT_REPO_DIR):
                    repos = [d for d in os.listdir(GIT_REPO_DIR) 
                            if os.path.isdir(os.path.join(GIT_REPO_DIR, d)) and d.endswith('.git')]
                    for repo in sorted(repos):
                        repo_name = repo.replace('.git', '')
                        html += f'<li><a href="/{repo_name}">{repo_name}</a>'
                        html += f'<span class="repo-actions">'
                        html += f'<a href="/{repo_name}.git">[Clone]</a>'
                        html += f'</span></li>\n'
                
                html += """        </ul>
    </div>
</body>
</html>"""
                self.wfile.write(html.encode('utf-8'))
            else:
                self.send_error(404, "Not found")
    
    def log_message(self, format, *args):
        """Override to log to stdout"""
        sys.stdout.write("%s - - [%s] %s\n" %
                        (self.address_string(),
                         self.log_date_time_string(),
                         format % args))

def main():
    """Start the git HTTP server"""
    if not os.path.exists(GIT_REPO_DIR):
        print(f"Error: Git repository directory not found: {GIT_REPO_DIR}")
        sys.exit(1)
    
    if not os.path.exists(GIT_HTTP_BACKEND):
        print(f"Error: git-http-backend not found: {GIT_HTTP_BACKEND}")
        sys.exit(1)
    
    server_address = ('', SERVER_PORT)
    httpd = http.server.HTTPServer(server_address, GitHTTPRequestHandler)
    
    print(f"Git HTTP Server starting on port {SERVER_PORT}")
    print(f"Serving repositories from: {GIT_REPO_DIR}")
    print(f"Access repositories at: http://localhost:{SERVER_PORT}/<repo-name>.git")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()

if __name__ == '__main__':
    main()

