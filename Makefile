export PLAYBOOK_VAULT_DIR?=../vault

config:
	test -f /etc/ansible/ansible.cfg && cat /etc/ansible/ansible.cfg | tail -n +2 >> ansible.cfg

check:
	# invoke dry-run

	ansible-playbook -i ${PLAYBOOK_VAULT_DIR}/production.ini ./site.yml --check

dhcpd:
	# run only dhcpd

	ansible-playbook -i ${PLAYBOOK_VAULT_DIR}/production.ini ./site.yml --limit dhcpd

lxd:
	# run only lcd's

	ansible-playbook -i ${PLAYBOOK_VAULT_DIR}/production.ini ./site.yml --limit lxd

dom0:
	# invoke real-run

	ansible-playbook -i ${PLAYBOOK_VAULT_DIR}/production.ini ./site.yml --limit dom0
