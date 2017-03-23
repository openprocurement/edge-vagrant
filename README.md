# edge-vagrant
## System min. requirements (sandbox):
* RAM: 2GB;
* HDD: 30 GB;
* CPU: DualCore

## Requirements:
* [Vagrant](https://www.vagrantup.com/docs/getting-started/);
* [Ansible from v2.2.0.0](http://docs.ansible.com/ansible/intro.html).

## Usage:
1. Change in vars/edge.yml `user_agent`;
2. Set in vars/edge.yml `resources`: example `resource: [tenders, plans, contracts]`. Allowed values (auctions, contracts, plans, tenders)

3. From directory where placed Vagrant file run command in terminal:
  ```
  vagrant up --provider=<your_provider>
  ```
  example:
  ```
  vagrant up --provider=virtualbox
  ```

4. API data available on:
  ```
  http://127.0.0.1:10001/api/2.3/<resource>
  ```
  `<resource>` can be `tenders`, `plans`, `contracts`, `auctions`

5. Edge activity available on `http:/127.0.0.1:10001/`

More informations: https://www.vagrantup.com/docs/providers/
